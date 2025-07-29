# cython: embedsignature=True, annotation_typing=False
# ----- moruapp_ms_sso/sso.py -----
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_sso.sso.microsoft import MicrosoftSSO
import jwt

from .config import Settings

# ルーターと設定の初期化
token_router = APIRouter(prefix="/auth", tags=["sso"])
settings = Settings()

# Azure callback 用ホスト名/URI
host_for_callback = (
    "localhost"
    if settings.host in ("0.0.0.0", "::0")
    else settings.host
)
backend_callback = f"http://{host_for_callback}:{settings.port}/auth/callback"

# Microsoft SSO クライアント
_sso = MicrosoftSSO(
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    tenant=settings.tenant_id,
    redirect_uri=backend_callback,
    allow_insecure_http=settings.allow_insecure_http,
)

# JWT チェック用セキュリティスキーム
security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> Optional[Dict[str, Any]]:
    """
    Cookie または Authorization ヘッダーから JWT を読み取り、ユーザー情報をデコードして返す。
    認証情報がなければ None を返す。
    """
    token = (
        credentials.credentials
        if credentials and credentials.credentials
        else request.cookies.get(settings.jwt_cookie_name)
    )
    if not token:
        return None
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None


def require_login(login_path: Optional[str] = None):
    """
    Depends で使用できる依存関数を生成。
    - 認証済みの場合: デコードした JWT ペイロード(dict) を返す
    - 未認証の場合: login_path または settings.login_url にリダイレクト (307)
    """
    async def _guard(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    ) -> Dict[str, Any]:
        user = await get_current_user(request, credentials)
        if not user:
            target = login_path or settings.login_url
            # FastAPI の HTTPException でリダイレクト
            raise HTTPException(status_code=307, headers={"Location": target})
        return user

    return Depends(_guard)

# 認証ルート
@token_router.get("/login")
async def login(
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user),
):
    # 認証済みならログイン処理をスキップしてフロントエンドへ
    if current_user:
        return RedirectResponse(url=settings.frontend_redirect_uri, status_code=302)

    # 未認証なら Azure 認可コード取得へ
    async with _sso:
        return await _sso.get_login_redirect()

@token_router.get("/callback")
async def callback(request: Request):
    # Azure から code を受け取り、ユーザー情報を取得
    async with _sso:
        user = await _sso.verify_and_process(request)

    # Pydantic BaseModel or dict を平坦化
    if hasattr(user, "dict"):
        user_data = user.dict()
    elif isinstance(user, dict):
        user_data = user
    else:
        user_data = user.__dict__

    # JWT 発行
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_expire_seconds)
    payload = {**user_data, "exp": expire}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    secure_flag = not settings.allow_insecure_http
    samesite_flag = "lax" if settings.allow_insecure_http else "none"
    response = RedirectResponse(url=settings.frontend_redirect_uri, status_code=302)
    response.set_cookie(
        key=settings.jwt_cookie_name,
        value=token,
        httponly=True,
        secure=secure_flag,
        samesite=samesite_flag,
        path="/",
        max_age=settings.jwt_expire_seconds,
    )
    return response

@token_router.post("/logout")
async def logout():
    secure_flag = not settings.allow_insecure_http
    samesite_flag = "lax" if settings.allow_insecure_http else "none"

    resp = JSONResponse({"detail": "Logged out"})
    resp.delete_cookie(
        key=settings.jwt_cookie_name,
        path="/",
        httponly=True,
        secure=secure_flag,
        samesite=samesite_flag,
    )
    return resp

@token_router.get("/user")
async def user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return current_user


def include_sso(app):
    # CORS はアプリ側で設定
    app.include_router(token_router)

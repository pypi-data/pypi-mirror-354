from fastapi import FastAPI
from .sso import token_router as sso_router, require_login, get_current_user
from .config import Settings

__version__ = "0.1.14"

# include_sso に login_url オプションを追加しています（必要なら設定を上書き）
def include_sso(app: FastAPI, *, login_url: str | None = None):
    settings = Settings()
    if login_url:
        settings.login_url = login_url
    app.include_router(sso_router)

__all__ = ["include_sso", "Settings", "sso_router", "require_login", "get_current_user"]
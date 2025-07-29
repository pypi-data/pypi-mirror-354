# setup.py
from setuptools import setup, Extension, find_packages
from setuptools.command.build_py import build_py as _build_py
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from Cython.Build import cythonize
import os

class build_py(_build_py):
    def run(self):
        super().run()
        # build_lib 配下から .py ファイルを削除
        for pkg in self.packages or []:
            pkg_dir = os.path.join(self.build_lib, *pkg.split('.'))
            if os.path.isdir(pkg_dir):
                for fname in os.listdir(pkg_dir):
                    if fname.endswith('.py'):
                        os.remove(os.path.join(pkg_dir, fname))

class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        # Wheel を pure-python ではなくバイナリ配布としてマーク
        self.root_is_pure = False

extensions = [
    Extension("moruapp_ms_sso.sso", ["moruapp_ms_sso/sso.py"]),
    Extension("moruapp_ms_sso.config", ["moruapp_ms_sso/config.py"]),
    Extension("moruapp_ms_sso.__main__", ["moruapp_ms_sso/__main__.py"]),
    Extension("moruapp_ms_sso.__init__", ["moruapp_ms_sso/__init__.py"]),
]

setup(
    name="moruapp-ms-sso",
    version="0.1.16",
    packages=find_packages(),
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3", "embedsignature": True},
    ),
    include_package_data=False,
    zip_safe=False,
    cmdclass={
        'build_py': build_py,
        'bdist_wheel': bdist_wheel,
    },
    install_requires=[
        "fastapi>=0.95",
        "uvicorn",
        "fastapi-sso",
        "python-dotenv",
        "pydantic-settings",
        "PyJWT",
    ],
)

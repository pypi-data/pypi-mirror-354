# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("moruapp_ms_sso.sso",       ["moruapp_ms_sso/sso.py"]),
    Extension("moruapp_ms_sso.config",    ["moruapp_ms_sso/config.py"]),
    Extension("moruapp_ms_sso.__main__",  ["moruapp_ms_sso/__main__.py"]),
    Extension("moruapp_ms_sso.__init__",  ["moruapp_ms_sso/__init__.py"]),
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3", "embedsignature": True},
    ),
)

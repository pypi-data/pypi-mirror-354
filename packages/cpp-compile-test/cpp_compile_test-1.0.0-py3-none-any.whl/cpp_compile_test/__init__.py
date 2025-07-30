# cpp_compile_test/__init__.py

try:
    from importlib.metadata import version
    __version__ = version("cpp-compile-test")
except Exception:
    __version__ = "unknown"
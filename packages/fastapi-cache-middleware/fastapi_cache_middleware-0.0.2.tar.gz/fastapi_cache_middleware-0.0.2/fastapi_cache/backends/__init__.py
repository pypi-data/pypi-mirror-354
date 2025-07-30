from fastapi_cache.types import Backend

__all__ = ["Backend"]

try:
    from fastapi_cache.backends import redis
except ImportError:
    pass
else:
    __all__ += ["redis"]

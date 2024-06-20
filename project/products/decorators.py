from functools import wraps

from django.conf import settings
from django.views.decorators.cache import cache_page


def cache_production(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view_func(*args, **kwargs):
            if settings.DEBUG:
                return view_func(*args, **kwargs)
            return cache_page(timeout)(view_func)(*args, **kwargs)
        return _wrapped_view_func
    return decorator

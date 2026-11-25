from rest_framework.permissions import SAFE_METHODS
from rest_framework.throttling import SimpleRateThrottle


class DemoReadThrottle(SimpleRateThrottle):
    scope = "demo_read"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": "shared-demo"}


class DemoWriteThrottle(SimpleRateThrottle):
    scope = "demo_write"

    def get_cache_key(self, request, view):
        if request.method in SAFE_METHODS:
            return None
        return self.cache_format % {"scope": self.scope, "ident": "shared-demo"}

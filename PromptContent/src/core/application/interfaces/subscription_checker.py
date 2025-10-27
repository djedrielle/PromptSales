from typing import Protocol

class SubscriptionChecker(Protocol):
    def is_allowed(self, tenant_id: str, feature: str) -> bool: ...

from src.core.application.interfaces.subscription_checker import SubscriptionChecker

class BillingAdapter(SubscriptionChecker):
    def __init__(self, base_url: str, token: str): ...
    def is_allowed(self, tenant_id: str, feature: str) -> bool:
        # TODO: call Portal/Subscriptions or return True in dev
        raise NotImplementedError

# src/core/application/interfaces/authorizer.py
from typing import Protocol

class IAuthorizer(Protocol):
    def can(self, actor_id: str, action: str, resource: str, tenant: str) -> bool: ...

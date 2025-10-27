from rest_framework.permissions import BasePermission

class CanManageBriefs(BasePermission):
    def has_permission(self, request, view):
        u = getattr(request, "user", None)
        scopes = getattr(u, "scopes", []) if u and getattr(u, "is_authenticated", False) else []
        return "briefs:write" in scopes or "admin" in scopes

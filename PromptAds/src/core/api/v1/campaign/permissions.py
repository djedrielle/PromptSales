# src/api/v1/campaign/permissions.py
from rest_framework.permissions import BasePermission

class CanManageCampaigns(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and "campaigns:write" in getattr(request.user, "scopes", [])

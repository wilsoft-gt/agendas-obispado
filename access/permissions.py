from rest_framework.permissions import BasePermission
from access.models import AuthToken

class AccessTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return True
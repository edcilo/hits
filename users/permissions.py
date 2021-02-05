from rest_framework.permissions import BasePermission

from users.models import User


class CanManageHits(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                user_type__in=[User.BIGBOSS, User.MANAGER]
            )
        except User.DoesNotExist:
            return False
        return True

class IsBigbossUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                user_type=User.BIGBOSS
            )
        except User.DoesNotExist:
            return False
        return True

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                user_type=User.MANAGER
            )
        except User.DoesNotExist:
            return False
        return True

class IsHitmanUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                user_type=User.HITMAN
            )
        except User.DoesNotExist:
            return False
        return True

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


class CanRegisterUser(BasePermission):
    def has_permission(self, request, view):
        user_type = request.data['user_type']
        user_auth = request.user

        if user_auth.is_bigboss() and not user_type == User.BIGBOSS:
            return True
        elif user_auth.is_manager() and user_type == User.HITMAN:
            return True
        else:
            return False


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

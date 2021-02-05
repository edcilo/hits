from rest_framework.permissions import BasePermission

from users.models import User


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


class CanDeactivateUser(BasePermission):
    def has_permission(self, request, view):
        user_auth = request.user
        user = request.resolver_match.kwargs.get('pk')

        try:
            user = User.objects.get(
                pk=user,
                is_active=True
            )
        except User.DoesNotExist:
            return False

        if user.pk == user_auth.pk:
            return False

        if user_auth.is_bigboss() or user_auth.pk == user.manager.pk:
            return True

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

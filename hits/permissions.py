from rest_framework.permissions import BasePermission

from users.models import User
from hits.models import Hit


class CanManageHits(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                user_type__in=[User.BIGBOSS, User.MANAGER]
            )
            hitman = User.objects.get(
                pk=request.data['hitman'],
                is_active=True
            )
        except User.DoesNotExist:
            return False

        if hitman.pk == user.pk:
            return False

        if user.is_bigboss():
            return True
        elif user.is_manager() \
            and hitman.user_type == User.HITMAN \
            and hitman.manager.pk == user.pk:
            return True

        return False


class CanChangeHitStatus(BasePermission):
    def has_permission(self, request, view):
        user_auth = request.user
        hit = request.resolver_match.kwargs.get('pk')

        if user_auth.is_bigboss():
            return True
        elif user_auth.is_manager():
            try:
                hit = Hit.objects.get(pk=hit, manager=user_auth)
                return True
            except Hit.DoesNotExist:
                return False

        return False

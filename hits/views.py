from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsBigbossUser
from hits.permissions import CanManageHits, CanChangeHitStatus

from hits.models import Hit
from hits.serializers import (HitModelSerializer, HitSerializer, HitChangeStatusSerializer)


# Create your views here.
class HitViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    serializer_class = HitModelSerializer

    def get_queryset(self):
        queryset = Hit.objects.filter(manager=self.request.user)
        return queryset

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes.append(CanManageHits)
        if self.name == 'change_status':
            permission_classes.append(CanChangeHitStatus)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = HitSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        hit = serializer.save()
        data = HitModelSerializer(hit).data
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        manager = Hit.objects.all() if self.request.user.is_bigboss() else Hit.objects.filter(manager=self.request.user)
        assigned = Hit.objects.filter(hitman=self.request.user)

        manager = HitModelSerializer(manager, many=True).data
        assigned = HitModelSerializer(assigned, many=True).data

        data = {
            "assigned": assigned,
            "manager": manager,
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user

        try:
            hit_id = request.resolver_match.kwargs.get('pk')

            if user.is_bigboss():
                hit = Hit.objects.get(pk=hit_id)
            elif user.is_manager():
                hit = Hit.objects.get(pk=hit_id, manager=user)
            elif user.is_hitman():
                hit = Hit.objects.get(pk=hit_id, hitman=user)
        except Hit.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        hit = HitModelSerializer(hit).data

        return Response(hit, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='change_status')
    def change_status(self, request, pk=None):
        hit = Hit.objects.get(pk=pk)
        serializer = HitChangeStatusSerializer(hit, request.data)
        serializer.is_valid(raise_exception=True)
        hit = serializer.save()
        data = HitModelSerializer(hit).data
        return Response(data, status=status.HTTP_200_OK)

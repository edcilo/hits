from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsBigbossUser, CanManageHits

from hits.models import Hit
from hits.serializers import (HitModelSerializer, HitSerializer)


# Create your views here.
class HitViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    serializer_class = HitModelSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes.append(CanManageHits)

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

    def get_queryset(self):
        queryset = Hit.objects.filter(manager=self.request.user)
        return queryset

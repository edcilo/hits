from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import CanRegisterUser, CanDeactivateUser
from users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, UserDeactiveSerializer
from users.models import User


# Create your views here.
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    def get_permissions(self):
        permission_classes = []

        if self.name == 'register':
            permission_classes = [IsAuthenticated, CanRegisterUser]
        elif self.name == 'logout':
            permission_classes = [IsAuthenticated]
        elif self.name == 'deactive':
            permission_classes = [IsAuthenticated, CanDeactivateUser]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], name='register')
    def register(self, request):
        user = request.user
        serializer = UserSignUpSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name='logout')
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], name='deactive')
    def deactive(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserDeactiveSerializer(user, request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

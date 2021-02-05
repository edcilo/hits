from django.contrib.auth import password_validation, authenticate, get_user_model
from django.core.validators import RegexValidator, FileExtensionValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from users.models import User


User = get_user_model()

class ManagerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class UserModelSerializer(serializers.ModelSerializer):
    manager = ManagerModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'user_type',
            'manager',
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(min_length=6, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

        user_type = data['user_type']
        if user_type == User.BIGBOSS:
            raise serializers.ValidationError("El tipo de usuario es invalido")

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user

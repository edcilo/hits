from rest_framework import serializers

from hits.models import Hit
from users.models import User
from users.serializers import UserModelSerializer


class HitModelSerializer(serializers.ModelSerializer):
    hitman = UserModelSerializer(read_only=True)
    manager = UserModelSerializer(read_only=True)

    class Meta:
        model = Hit
        fields = (
            'pk',
            'target',
            'description',
            'status',
            'created_at',
            'last_modified',
            'hitman',
            'manager',
        )

class HitSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=10000)
    target = serializers.CharField(max_length=255)
    hitman = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, data):
        hit = Hit.objects.create(**data)
        return hit

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    BIGBOSS = 'BB'
    MANAGER = 'MG'
    HITMAN = 'HM'

    USER_TYPES = [
        (BIGBOSS, 'Bigboss'),
        (MANAGER, 'Manager'),
        (HITMAN, 'Hitman'),
    ]

    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default=HITMAN,
    )

    def is_bigboss(self):
        return this.user_type is self.BIGBOSS

    def is_manager(self):
        return this.user_type is self.MANAGER

    def is_hitman(self):
        return this.user_type is self.HITMAN

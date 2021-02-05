from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
    manager = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def is_bigboss(self):
        return self.user_type in {self.BIGBOSS,}

    def is_manager(self):
        return self.user_type in {self.MANAGER,}

    def is_hitman(self):
        return self.user_type in {self.HITMAN,}

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = self.BIGBOSS

        if not self.is_superuser and self.user_type == self.BIGBOSS:
            self.user_type = self.HITMAN

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if not self.is_bigboss():
            super(User, self).delete(using, keep_parents)

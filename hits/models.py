from django.db import models
from users.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Hit(models.Model):
    """Assassination system."""

    CLOSED = 'c'
    FAILED = 'f'
    OPEN = 'o'

    STATUS_TYPES = [
        (CLOSED, 'Closed'),
        (FAILED, 'Failed'),
        (OPEN, 'Open'),
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS_TYPES,
        default=OPEN,
    )
    target = models.CharField(max_length=255)
    description = RichTextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    hitman = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hit_assigned')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hit_created')

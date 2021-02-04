from django.contrib import admin

from users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ('pk', 'username', 'email', 'user_type',)
    list_display_links = ('pk', 'username', 'email', 'user_type',)

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
    )

    readonly_fields = ('date_joined',)

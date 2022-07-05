from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Follow

User = get_user_model()


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = (
        'user__username', 'author__username',
        'user__email', 'author__email'
    )
    list_filter = (
        'user', 'author',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'id',
    )
    search_fields = (
        'username', 'first_name',
        'last_name', 'id',
    )
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)

from email.headerregistry import Group
from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'id',
    )
    search_fields = ('username', 'first_name', 'last_name', 'id')
    list_filter = ('email','username',)
    empty_value_display = '-пусто-'
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
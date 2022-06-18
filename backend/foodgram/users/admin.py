from django.contrib import admin

class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name'
        'email',
        'id',
    )
    list_editable = ('username',)
    search_fields = ('username', 'first_name', 'last_name', 'id')
    list_filter = ('id',)
    empty_value_display = '-пусто-'
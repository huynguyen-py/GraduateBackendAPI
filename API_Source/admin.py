from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_verified', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('create_at', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password',('username', 'avatar'))}),
        ('Permissions', {'fields': (('is_staff', 'is_verified'), ('is_active' , 'is_superuser'), )}),
        ('Important dates',{'fields': ('last_login',)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions', 'first_name', 'last_name', 'phone', 'address', 'Followed'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),   # class for css
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}     # fields shown on create user page on admin panel
        ),
    )

    search_fields = ('email',)     #search_filter for search bar
    ordering = ('email',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
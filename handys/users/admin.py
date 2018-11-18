from django.contrib import admin

from users.models import PermissionLevel1, PermissionLevel2, User


@admin.register(User)
class ParentPermissionAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'created_at', 'updated_at']
    list_filter = ['created_at']


@admin.register(PermissionLevel1)
class ParentPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_available']
    list_filter = ['created_at', 'name']


@admin.register(PermissionLevel2)
class ParentPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_available']
    list_filter = ['created_at', 'name']

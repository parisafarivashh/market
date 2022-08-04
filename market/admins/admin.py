from django.contrib import admin

# Register your models here.
from admins.models import Admin, AdminPermissions


@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'username', 'super_admin']
    list_filter = ['id', 'super_admin', 'email', 'first_name']
    search_fields = ['username__startswith', 'first_name__startswith']
    readonly_fields = ['phone_number', 'username', 'last_login']


@admin.register(AdminPermissions)
class CustomAdminPermission(admin.ModelAdmin):
    list_display = ['admin_id', 'manage_admins']
    list_filter = ['id', 'manage_admins', 'admin_id', 'admin_id__username']
    search_fields = ['admin_id__username__startswith',
                     'admin_id__first_name__startswith']
    readonly_fields = ['admin_id']


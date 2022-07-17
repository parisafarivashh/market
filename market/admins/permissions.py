from rest_framework.permissions import BasePermission

from .models import Admin


class IsAdmin(BasePermission):
    message = 'You Are Not Admin.'

    def has_permission(self, request, view):
        return type(request.user) == Admin


class IsOwnProfileAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ManageAdmins(BasePermission):
    message = 'You Can Not Manage Admins'

    def has_permission(self, request, view):
        return request.user.super_admin or request.user.adminpermissions.manage_admins


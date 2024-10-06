from rest_framework.permissions import BasePermission


class IsOwn(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id != obj.creator.id:
            return False


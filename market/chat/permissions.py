from rest_framework.permissions import BasePermission


class CantSeenOwnMessage(BasePermission):
    message = 'User Can not Seen Own Message'

    def has_object_permission(self, request, view, obj):
        return obj.sender != request.user


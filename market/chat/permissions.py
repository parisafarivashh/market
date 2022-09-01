from rest_framework.permissions import BasePermission


class CanNotSeenOwnMessage(BasePermission):
    message = 'User Can not Seen Own Message'

    def has_object_permission(self, request, view, obj):
        return obj.sender != request.user


class OwnMessage(BasePermission):
    message = 'Message dose not exit'

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
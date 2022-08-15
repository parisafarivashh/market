from rest_framework.permissions import BasePermission


class IsUserProfile(BasePermission):
    message = 'You only access to own profile '

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True


class IsSeller(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.seller == request.user:
            return True


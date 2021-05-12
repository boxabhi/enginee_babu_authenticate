"""
Author: Sanidhya Mangal, Ravinder Singh
github:sanidhyamangal
email: sanidhya.mangal@engineerbabu
"""
from rest_framework import permissions


# create IsOwner Method
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    A custom class to allow users to view only if the the user is
    owner of that object
    """
    def has_object_permission(self, request, view, obj):

        # check if the request is in safe methods

        return obj.uid == request.user.uid


class IsSuperAdminOrStaff(permissions.BasePermission):
    """
    A custom class to check if user is admin or staff
    """
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser and \
            request.user.has_perm("authentication.all_permissions")


class IsOwnerAttributes(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.uid == request.user.uid

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsManager(permissions.BasePermission):
    """
    Permission class to check if the person is manager or not
    """
    def has_permission(self, request, view):
        return request.user.is_manager


class BaseViewSetPermissionMixin:
    def get_permissions(self):
        if self.action == 'list':
            permission_class = [permissions.IsAuthenticated]
        elif self.action in [
                'login', 'signup', 'forgot_password', 'reset_password'
        ]:
            permission_class = []
        else:
            permission_class = [IsOwnerAttributes]
        return [permission() for permission in permission_class]

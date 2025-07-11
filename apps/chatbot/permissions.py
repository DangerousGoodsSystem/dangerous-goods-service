from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoModelPermissions

class IsAdminUser(BasePermission):
    """
    Admin only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsStaffUser(BasePermission):
    """
    Admin or Staff only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
    
class IsUser(BasePermission):
    """
    User only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
class DjangoModelPermissionsWithView(DjangoModelPermissions):
    perms_map = {
        'GET':     ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD':    ['%(app_label)s.view_%(model_name)s'],
        'POST':    ['%(app_label)s.add_%(model_name)s'],
        'PUT':     ['%(app_label)s.change_%(model_name)s'],
        'PATCH':   ['%(app_label)s.change_%(model_name)s'],
        'DELETE':  ['%(app_label)s.delete_%(model_name)s'],
    }
from user.api.permission.base_group_permission import BaseGroupPermission
from rest_framework import permissions


class IsSuperUser(BaseGroupPermission):
    """
    Check if user's group is Admin and Authenticated
    """
    
    #  class attribute: group name for Admin
    allowed_groups = ["SuperUser"]

    # def has_permission(self, request, view):
    #     """
    #     Check if the user has permission to perform the action.
    #     """
    #     if request.method in permissions.SAFE_METHODS: # SAFE_METHODS: GET, HEAD method but not PUT, POST, DELETE
    #         # Check permissions for READ-ONLY request
    #         return True

    #     return bool(request.user and self.has_group_permission(request.user))
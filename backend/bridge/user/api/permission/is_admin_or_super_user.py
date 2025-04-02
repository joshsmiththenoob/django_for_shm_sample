from user.api.permission.base_group_permission import BaseGroupPermission
from rest_framework import permissions


class IsAdminOrSupoerUser(BaseGroupPermission):
    """
    Check if user's group is Admin and Authenticated
    """
    
    #  class attribute: group name for Admin, SuperUser
    allowed_groups = ["Admin", "SuperUser"]

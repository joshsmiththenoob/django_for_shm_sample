from rest_framework import permissions
from django.contrib.auth.models import Group

class BaseGroupPermission(permissions.BasePermission):
    """
    A base class for group-based permissions.
    Subclasses must define `allowed_groups`.
    """

    allowed_groups = []

    def __init__(self):
        """
        Checks if allowed groups were set in subclasses
        """
        if not (self.allowed_groups):
            raise ValueError(f"{self.__class__.__name__} must define allowed_groups")
        
    
    def __is_in_group(self, user: str, group: str):
        """
        Cheks if the user belongs to a specific group.
        """

        try:
            return Group.objects.get(name= group).user_set.filter(id= user.id).exists()
        except Group.DoesNotExist:
            print(Group.DoesNotExist)
            return False
        
    def has_group_permission(self, user: str):
        """
        Checks if the user belongs to any of the allowed groups
        """
        return any([self.__is_in_group(user, group) for group in self.allowed_groups])
    

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        """
        if (request.method in permissions.SAFE_METHODS) and (request.user.is_authenticated): # SAFE_METHODS: GET, HEAD method but not PUT, POST, DELETE
            # Check permissions for READ-ONLY request
            return True

        return bool(request.user and self.has_group_permission(request.user))
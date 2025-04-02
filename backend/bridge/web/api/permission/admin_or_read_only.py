from rest_framework import permissions

class AdminOrReadyOnly(permissions.IsAdminUser):
    """
    Using the custom permission class to introduce
    1. if user is admin, he can check
    """
    def has_permission(self, request, view):
        """
        1. All staffs can access it if use GET Method to read
        2. Admin(parent class) can do anything
        """
        # return ((request.method == "GET") or (super().has_permission(request, view)))
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            print((request.user and request.user.is_staff))
            return (request.user and request.user.is_staff)

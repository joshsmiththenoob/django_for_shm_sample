from rest_framework import permissions

class BridgeUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        has object permission can check
        if ORM object's (like User) imformation is same as request's user name
        
        ex: we can check if the article (ORM object) is belong to john
            1. we can compare Article's author name to request user name
            2. if True: we can let the original author to edit this post  
        """
        print(request.method)
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS: GET, HEAD method but not PUT, POST, DELETE
            # Check permissions for READ-ONLY request
            return True
        else:
            # Check permissions for POST, PUT, DELETErequest
            # if the user was the owner or not 
            
            return (str(request.user) == "john") # request.user is the user who's current logged in
            # return obj.review_user == request.user
        # return super().has_object_permission(request, view, obj)
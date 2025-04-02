# Customize Login View From DRF-simpleJWT to create and take JWT in Cookie
from rest_framework.permissions import (IsAuthenticated, 
                                        AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView
from bridge.utils.response_formatter import ResponseFormatter

class LogoutView(APIView):
    """
    API for user logout without verifying authentication tokens.
    
    This view allows users to logout without checking if their cookies 
    (access_token or refresh_token) are valid. 
    It is designed to enable forced logouts or manual logouts 
    without requiring token validation.
    """
    permission_classes = [AllowAny]
    authentication_classes = [] # Disable global setting of authentication check (e.g., CookiesJWTAuthentication)
    
    def post(self, request):
        json = dict()

        try:
            json = ResponseFormatter.format_post_response(None, with_login= True)
            response_json = Response(json)
            # Delete Cookies of AT, RT
            response_json.delete_cookie(key= "access_token",
                                        path= "/",
                                        samesite= None)
            response_json.delete_cookie(key= "refresh_token",
                                        path= "/",
                                        samesite= None)
            
        except:
            json = ResponseFormatter.format(False, "Login Failed")
            response_json = Response(json)

        return response_json

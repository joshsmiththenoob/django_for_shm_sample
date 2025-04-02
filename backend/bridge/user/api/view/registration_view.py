# import user.models
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from bridge.utils.swagger_decorator import auto_schema_with_example # import decorator for SwaggerUI Example
from user.api.service.registration_service import RegistrationService
from rest_framework.response import Response
from user.api.serializer.registration_serializer import RegistrationSerializer
from user.api.handler.cookie_handler import CookieHandler

class RegistrationView(APIView):
    """
    API for user registration.

    Handles user registration and returns user information, 
    including access and refresh JSON web tokens (JWT). 
    Authentication checks are disabled to allow new users to register 
    without requiring pre-existing authentication.
    """
    authentication_classes = [] # Disable global setting of authentication check (e.g., CookiesJWTAuthentication)
    permission_classes = [AllowAny]
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @auto_schema_with_example(RegistrationSerializer)
    def post(self, request):
        
        regis_s = RegistrationService()
        cookie_handler = CookieHandler()

        # package token with Cookies
        json = regis_s.register_user(request)
        access_token = json["token"]["access"]
        refresh_token = json["token"]["refresh"]

        response_json = Response(json)  

        cookie_handler.set_cookies(response_json, {"access_token": access_token,
                                                   "refresh_token": refresh_token})


        return response_json
# Customize Refresh Token View From DRF-simpleJWT to create and take JWT in Cookie
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.request import Request
from rest_framework.response import Response
from user.api.handler.cookie_handler import CookieHandler


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):  #**kwargs: like unpack the dict varaible called kwargs: {"username": ..., "password": ...}
        # form response json
        json = dict()
        cookie_handler = CookieHandler()
        try:
            # validate if refresh token is correct or not
            refresh_token = request.COOKIES.get("refresh_token")

            # let request body:dict include refresh token (key-value pair: "refresh": ...) that refresh API will return Access Token
            request.data["refresh"] = refresh_token

            # get new access token
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            # parse json from resposne returned by parent class' post method
            # the returned JSON of JWT will be {"access_token":..., "refresh_token":...}
            access_token = tokens["access"]

            json["response"] = "Successful"

            # set Cookies for access token and refresh token
            response_json = Response(json)

            cookie_handler.set_cookies(response_json, {"access_token": access_token})

        except Exception as e: 
            print(e)
            json["response"] = "Authentication credentials were not provided."
            response_json = Response(data= json)

        return response_json    
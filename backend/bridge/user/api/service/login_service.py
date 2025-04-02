# Customize Login View From DRF-simpleJWT to create and take JWT in Cookie
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from user.api.handler.cookie_handler import CookieHandler
from bridge.utils.response_formatter import ResponseFormatter

class LoginService(TokenObtainPairView):

    
        
    def login(self, request, *args, **kwargs):
        cookie_handler = CookieHandler()
        try:
            
            # get JWT from returning the resposne object(Json) from parent class' method: post
            response = super().post(request, *args, **kwargs) 
            tokens = response.data

            # parse json from resposne returned by parent class' post method
            # the returned JSON of JWT will be {"access_token":..., "refresh_token":...}
            access_token = tokens["access"]
            refresh_token = tokens["refresh"]

            # Get the username from the request data (json/dict)
            username = request.data.get("username")


            # Trigger user_logged_in signal to update login statement(last login time)
            user = User.objects.get(username= username)
            user_logged_in.send(sender= user.__class__, 
                                request= request, 
                                user= user)

            response_json = ResponseFormatter.format_post_response(None, with_login= True)

            # set Cookie of access token
            cookie_handler.set_cookies(response_json, {"access_token": access_token,
                                                "refresh_token": refresh_token})
            

        except Exception as e: 
            print(e)
            response_json = ResponseFormatter.format_400_response(str(e))
        

        finally:
            # print("Cookies: \n", response_json.cookies)
            return response_json    
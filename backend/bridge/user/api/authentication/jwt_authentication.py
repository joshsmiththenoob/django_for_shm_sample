# Authentication: to check whether format of Cookies brought by frontend is correct or not.

from rest_framework_simplejwt.authentication import JWTAuthentication

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("進行驗證中")
        # get AT from Cookies on every requests

        access_token = request.COOKIES.get("access_token")
        if (access_token is None):
            return None
       
        # validate if token is correct or not/ expired
        validated_token = self.get_validated_token(access_token)
        
        # print(validated_token)
        
        # # return two-tuple of (user, token)
        # return self.get_user(validated_token), validated_token
        
        try:
            user = self.get_user(validated_token)
        except:
            return None
        

        return (user, validated_token)    
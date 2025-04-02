from rest_framework_simplejwt.tokens import RefreshToken
from user.api.serializer.registration_serializer import RegistrationSerializer


class RegistrationService:
    """
    Service class to handle user registration logic
    """
    serializer_class = RegistrationSerializer
    def register_user(self, request):
        serializer = self.serializer_class(data= request.data)
        json = dict()

        # check data is valid or not
        if serializer.is_valid():
            account_info = serializer.save() # receive User ORM object
            json["response"] = "Registration Successful!"
            json["username"] = account_info.username
            json["email"] = account_info.email

            # create token directly
            # # for creating token of Token Authentication
            # token = Token.objects.get(user= account_info).key # in table authtoken_token, the token is recorded in key column
            
            # json["token"] = token

            # for creating token of JWT Authentication
            refresh = RefreshToken.for_user(account_info)
            
            json["token"] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
            
        else:
            print(serializer.is_valid())
            # if request was not valid -> return serializer.error: dict 
            json = serializer.errors
        
        return json
    
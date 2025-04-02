# Serializer
"""
Serializer:
like DTO in SpringBoot, 
in charge of serialize (Object -> Json) de-serialize(Json -> Object) the data between frontend and backend

also check if the data structure is correct or not.

"""

from django.contrib.auth.models import User
from rest_framework import serializers
from drf_yasg import openapi

class RegistrationSerializer(serializers.ModelSerializer):
    # set style as input password & can write but cannot read for content
    password2 = serializers.CharField(style= {"input_type": "password"}, write_only= True) 
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"] # using password2 to check if password is correct or not
        
        # kwargs = key word arguments
        # the difference bettween serializer.data and serializer.validated_data is Django can hide info with write only statement
        extra_kwargs = {
            "password": {"write_only": True} # set password's mode for extra
        }
        
        # Define request body example in swagger doc.
        example = {
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="使用者名稱", example="example_user"
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="電子郵件", example="example@email.com"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="密碼",
                format="password",
                example="Password@123",
            ),
            "password2": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="再次輸入密碼",
                format="password",
                example="Password@123",
            ),
        }

    # override the save class from parent class
    def save(self):
       # serializer.save() will be called after serializer check if data is valid or not(serializer.valid())
       self.__validate_passwords()
       self.__check_if_email_is_unique()

       # save account info if two checks are passed
       # create new User ORM object
       account = User(email= self.validated_data["email"], username= self.validated_data["username"])
       account.set_password(self.validated_data["password"]) # call methods of object from parent class' method
       account.save()

        # return ORM object about user
       return account

    def __validate_passwords(self):
        # check if password and password2 are the same
        # validated_data's datatype is dictionary
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if (password != password2):
            raise serializers.ValidationError({"error": "Passwords should be same!"})
        
    def __check_if_email_is_unique(self):
        # check if email is unique from all existed users   
        if (User.objects.filter(email= self.validated_data["email"]).exists()):
            raise serializers.ValidationError({"error": "Email already exists!"})
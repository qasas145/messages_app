from rest_framework.authentication import BaseAuthentication
from .models import CustomUser
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class Authentication(BaseAuthentication) :


    def authenticate(self, request):
        data = self.validate_request(request.headers)

        if not data :
            return None, None



        return self.get_user(data['id']), None

    def get_user(self, id) :
        try :
            user = CustomUser.objects.get(id = id)
            return user

        except :
            return None

    def validate_request(self, headers) :
        authorization = headers.get("Authorization", None)

        if not authorization :
            return None

        token = headers['Authorization'][7:]
        decoded_data = Authentication.verify_token(token)

        if not decoded_data:
            return None

        return decoded_data
    @staticmethod
    def verify_token(token) :
        print(token)
        try :
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            print("hello")
        except Exception :
            return None

        exp = decoded_data["exp"]
        print(exp)

        if datetime.now().timestamp() > exp:
            print("no one")
            return None

        return decoded_data
            

        
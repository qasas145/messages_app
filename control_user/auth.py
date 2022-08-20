import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .models import CustomUser
import random
import string


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(data) :
    data = jwt.encode(
        {"exp" : datetime.now() + timedelta(minutes=40), **data},
        settings.SECRET_KEY,
        algorithm="HS256"
        
    )
    return data

def get_refresh_token() :
    data = jwt.encode(
        {"exp": datetime.now() + timedelta(hours=1), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return data

def decodeJWT(bearer) :
    if not bearer :
        return None
    
    token = bearer[7:]

    decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms="HS256"
        )
    if decoded :

        try :
            print(CustomUser.objects.get(id=decoded["user_id"]))
            return CustomUser.objects.get(id=decoded["user_id"])
        except Exception:
            return None

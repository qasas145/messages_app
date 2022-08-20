from rest_framework import serializers
from .models import CustomUser, Favorite, Jwt

class LoginSerializer(serializers.ModelSerializer) :
    username = serializers.CharField()
    password = serializers.CharField(style = {'input_type' : 'password'}, write_only = True, required = True)


    class Meta :
        model = CustomUser
        fields = ('username', 'password')

class RegisterSerializer(serializers.Serializer) :
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_image = serializers.ImageField()
    password = serializers.CharField(style = {'input_type': 'password'}, write_only = True, required = True)

    class Meta :
        model = CustomUser
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer) : # or serializers.Serializer
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style = {'input_type' : 'password'}, write_only = True, required = False)

    class Meta :
        model = CustomUser
        fields = ['id', 'username','email','first_name', 'last_name', 'profile_image','password']


class FavoriteSerializer(serializers.Serializer) :
    favorite_id = serializers.IntegerField()




class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


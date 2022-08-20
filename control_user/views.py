from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import filters
from django.contrib.auth.hashers import make_password, check_password
from message_control.models import GenericFileUpload
from django.db.models import Q, Count
import re
from chatapi2.custom_methods import IsAuthenticatedCustom, IsAuthenticated


# models 
from .models import CustomUser, Favorite, Jwt

#serializers
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, FavoriteSerializer, RefreshSerializer
from .auth import get_access_token, get_refresh_token
from .authentication import Authentication



class UserView(ModelViewSet) :
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedCustom]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    


class LoginView(APIView) :
    serializer_class = LoginSerializer

    def post(self, request) :
        

        serilaizer = self.serializer_class(data = request.data)
        serilaizer.is_valid(raise_exception=True)


        user = authenticate(
            username = serilaizer.validated_data['username'],
            password = serilaizer.validated_data['password']
        )


        if not user :
            return Response({"error": "Invalid username or password"}, status="400")
        
        Jwt.objects.filter(user = user.id).delete()

        access = get_access_token({'user_id' : user.id})
        refresh = get_refresh_token()
        print(refresh)


        Jwt.objects.create(user_id = user.id, access = access, refresh = refresh)

        return Response({"access": access, "refresh": refresh})

class LogoutView(APIView) :
    permission_classes = (IsAuthenticatedCustom,)

    def get(self, request) :
        
        Jwt.objects.filter(user = request.user.id).delete()

        return Response("logged out successfully", status=200)

class RegisterView(APIView) :

    serializer_class = RegisterSerializer

    http_method_names = ['post']

    def post(self, request) :
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        profile_image = request.data.pop("profile_image", None)


        profile_image = GenericFileUpload.objects.create(file_upload = profile_image[0])
        
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.validated_data['profile_image'] = profile_image

        CustomUser.objects.create(**serializer.validated_data)


        
        return Response({"success": "User created."}, status=201)

class UpdateFavoriteView(APIView) :
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = FavoriteSerializer

    http_method_names = ['post']
    def post(self, request) :
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        try :
            favorite_user = CustomUser.objects.get(id = serializer.validated_data['favorite_id'])
        except :
            raise Exception("Favorite user does not exist")

        try :
            fav = request.user.user_favorites
            print("hello")
        except :
            print("sayed")
            fav = Favorite.objects.create(user_id = request.user.id)

        favorite = fav.favorites.filter(id = favorite_user.id)

        if favorite :
            fav.favorites.remove(favorite_user)
            return Response("removed")
        fav.favorites.add(favorite_user)

        return Response("added")


class CheckIsFavoriteView(APIView):

    permission_classes = (IsAuthenticatedCustom,)

    def get(self, request, *args, **kwargs) :
        favorite_id = kwargs.get("favorite_id", None)
        try :
            fav = request.user.user_favorites.favorites.filter(id = favorite_id)
            print(fav)
            if fav :
                return Response(True)
            else :
                return Response(False)
        except Exception as e:
            return Response(False)



class RefreshView(APIView):
    serializer_class = RefreshSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})

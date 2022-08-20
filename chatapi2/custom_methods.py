from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone




class IsAuthenticated(BasePermission) :
    def has_permission(self, request, view):

        from control_user.auth import decodeJWT
        print(request.META['HTTP_AUTHORIZATION'])
        user = decodeJWT(request.META['HTTP_AUTHORIZATION']) 

        if not user :
            return False

        request.user = user

        if request.user and request.user.is_authenticated :
            from control_user.models import CustomUser

            CustomUser.objects.filter(id =  request.user.id).update(
                is_online = timezone.now()
            )
            return True
        return False

class IsAuthenticatedCustom(BasePermission) :
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS :
            return True
        if request.user and request.user.is_authenticated :
            from control_user.models import CustomUser
            CustomUser.objects.filter(id = request.user.id).update(
                is_online = timezone.now()
            )
            return True
        return False


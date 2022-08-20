from django.contrib import admin
from .models import Favorite, CustomUser, Jwt, CustomUserManager




class CustomUserAdmin(admin.ModelAdmin) :
    list_display = ['username','email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Favorite)
admin.site.register(Jwt)
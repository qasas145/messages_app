from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser, User
from django.utils import timezone
from message_control.models import GenericFileUpload



class CustomUserManager(BaseUserManager) :
    def create_user(
            self,
            username: str,
            email: str,
            first_name,
            last_name,
            password: str = None,
            is_staff=False,
            is_superuser=False,
        ) -> "CustomUser":
            if not email:
                raise ValueError("User must have an email")
            user = self.model(email=self.normalize_email(email))
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.is_active = True
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()

            return user

    def create_superuser(
            self, username, first_name, last_name, email: str, password: str
        ) -> "CustomUser":
            print(email, password)
            user = self.create_user(
                username = username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_staff=True,
                is_superuser=True,
            )

            return user



class CustomUser(AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(verbose_name = 'Email .',unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    profile_image = models.ForeignKey(GenericFileUpload, related_name = "user_image",on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.DateTimeField(default=timezone.now)

    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return f'{self.username}'

    class Meta : 
        ordering = ( "created_at", )


class Favorite(models.Model) :
    user = models.OneToOneField(CustomUser, related_name = 'user_favorites', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(CustomUser, related_name="user_favoured")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
    class Meta :
        ordering = ('created_at',)


class Jwt(models.Model) :
    user = models.OneToOneField(CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username}'



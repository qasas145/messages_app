from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutView, UserView, LoginView, RegisterView, RefreshView, CheckIsFavoriteView, UpdateFavoriteView

router = DefaultRouter()
router.register("users", UserView)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('update-favorite', UpdateFavoriteView.as_view()),
    path('check-favorite/<int:favorite_id>', CheckIsFavoriteView.as_view()),

]

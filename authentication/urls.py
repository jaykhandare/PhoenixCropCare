from django.urls import path
from authentication.views import register_user, login_view, logout_view

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', login_view, name="login"),
    path("logout/", logout_view, name="logout"),

]

from django.urls import path

from authentication.views import login_view, logout_view, register_user

urlpatterns = [
    path('register/', register_user, name="register"),
    path('accounts/login/', login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),

]

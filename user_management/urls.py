from django.urls import path
from user_management.views import all_users, profile, register_dealer, all_dealers

urlpatterns = [
    path('all_users/', all_users, name="all_users"),
    path('profile/', profile, name="profile"),
    path('register_dealer/', register_dealer, name="register_dealer"),
    path('all_dealers/', all_dealers, name="all_dealers"),
]

from django.urls import path
from user_management.views import all_users, profile, register_dealer, all_dealers, edit_dealer, remove_dealer, testFunction

urlpatterns = [
    path('all_users/', all_users, name="all_users"),
    path('profile/', profile, name="profile"),
    path('register_dealer/', register_dealer, name="register_dealer"),
    path('all_dealers/', all_dealers, name="all_dealers"),
    path('edit_dealer/', edit_dealer, name="edit_dealer"),
    path('remove_dealer/', remove_dealer, name="remove_dealer"),

    path('testFunction/', testFunction, name="testFunction"),
]

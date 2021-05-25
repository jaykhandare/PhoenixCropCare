from django.urls import path

from user_management.views import (all_dealers, all_users, edit_dealer,
                                   profile, register_dealer, remove_dealer,
                                   remove_user)

urlpatterns = [
    path('all_users/', all_users, name="all_users"),
    path('profile/', profile, name="profile"),
    path('register_dealer/', register_dealer, name="register_dealer"),
    path('all_dealers/', all_dealers, name="all_dealers"),
    path('edit_dealer/', edit_dealer, name="edit_dealer"),
    path('remove_dealer/', remove_dealer, name="remove_dealer"),
    path('remove_user/', remove_user, name="remove_user"),

]

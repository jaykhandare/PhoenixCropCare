from django.urls import path
from user_management.views import all_users, profile
urlpatterns = [
    path('all_users/', all_users, name="all_users"),
    path('profile/', profile, name="profile"),
]

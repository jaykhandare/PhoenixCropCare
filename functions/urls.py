from django.urls import path
from functions.views import home_view

urlpatterns = [
    path('home/', home_view, name="home_view"),
]

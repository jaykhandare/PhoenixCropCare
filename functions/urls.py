from django.urls import path

from functions.views import get_my_dealers, home_view, modify_tax_rates

urlpatterns = [
    path('home/', home_view, name="home_view"),
    path('my_dealers/', get_my_dealers, name="get_my_dealers"),
    path('modify_tax_rates/', modify_tax_rates, name="modify_tax_rates"),

]

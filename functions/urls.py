from django.urls import path

from functions.views import get_my_dealers, get_my_sales, home_view, modify_tax_rates

urlpatterns = [
    path('', home_view, name="home_redirect"),
    path('home/', home_view, name="home_view"),
    path('my_dealers/', get_my_dealers, name="get_my_dealers"),
    path('get_my_sales/', get_my_sales, name="get_my_sales"),
    path('modify_tax_rates/', modify_tax_rates, name="modify_tax_rates"),
]

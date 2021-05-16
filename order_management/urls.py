from django.urls import path
from order_management.views import add_product, get_product_list

urlpatterns = [
    path('add_product/', add_product, name="add_product"),
    path('get_product_list/', get_product_list, name="get_product_list"),

]

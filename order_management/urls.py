from django.urls import path
from order_management.views import add_product, add_item_to_cart, checkout, test

urlpatterns = [
    path('test/', test, name="test"),

    path('add_product/', add_product, name="add_product"),
    path('add_item_to_cart/', add_item_to_cart, name="add_item_to_cart"),
    path('checkout/', checkout, name="checkout"),

]

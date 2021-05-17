from django.urls import path
from order_management.views import add_product, add_item_to_cart, checkout

urlpatterns = [
    path('add_product/', add_product, name="add_product"),
    path('add_item_to_cart/', add_item_to_cart, name="add_item_to_cart"),
    path('checkout/', checkout, name="checkout"),

]

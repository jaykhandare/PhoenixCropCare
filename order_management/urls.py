from django.urls import path
from order_management.views import add_product, edit_product, remove_product, all_products, checkout, test

urlpatterns = [
    path('test/', test, name="test"),

    path('add_product/', add_product, name="add_product"),
    path('edit_product/', edit_product, name="edit_product"),
    path('remove_product/', remove_product, name="remove_product"),
    path('all_products/', all_products, name="all_products"),
    path('checkout/', checkout, name="checkout"),

]

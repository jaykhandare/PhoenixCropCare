from django.urls import path

from order_management.views import (add_product, all_products,
                                    all_transactions, checkout, edit_product,
                                    remove_product, test, view_transaction)

urlpatterns = [
    path('test/', test, name="test"),

    path('add_product/', add_product, name="add_product"),
    path('edit_product/', edit_product, name="edit_product"),
    path('remove_product/', remove_product, name="remove_product"),
    path('all_products/', all_products, name="all_products"),
    path('checkout/', checkout, name="checkout"),
    path('all_transactions/', all_transactions, name="all_transactions"),
    path('view_transaction/', view_transaction, name="view_transaction"),

]

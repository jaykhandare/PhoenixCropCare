from django.urls import path
from order_management.views import add_product

urlpatterns = [
    path('add_product/', add_product, name="add_product"),

]

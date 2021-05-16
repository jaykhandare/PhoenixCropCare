from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from order_management.models import Product, Order, Transaction
from user_management.support import is_staff

@login_required
def test(request):
    return render(request, "custom_templates/home.html")

@login_required
def add_product(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")
    
    if request.method == "GET":
        return render(request, "orders/add_product_form.html")
    elif request.method == "POST":
        product_data = request.POST.dict()
        msg = ""
        try:
            Product.objects.create(type=product_data['type'], name=product_data['name'], price=float(product_data['price']))
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            msg = "Product {} added".format(product_data['name'])
            return render(request, "orders/add_product_form.html", {"msg" : msg})

@login_required
def add_product_from_csv(request):
    pass


def get_product_list(request):
    pass


@login_required
def create_order(request):
    pass


@login_required
def checkout(request):
    pass
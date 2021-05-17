from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_management.support import is_staff
from order_management.models import Product, Order, Transaction
from order_management.support import generate_transaction_report, create_session_dict

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
        try:
            try:
                float(product_data['price'])
            except Exception as e:
                return render(request, "orders/add_product_form.html", {"msg" : "price should be in numbers"})
            Product.objects.create(type=product_data['type'], name=product_data['name'], price=float(product_data['price']))
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            msg = "Product {} added".format(product_data['name'])
            return render(request, "orders/add_product_form.html", {"msg" : msg})

@login_required
def add_products_from_csv(request):
    pass


@login_required
def add_item_to_cart(request):
    objects = Product.objects.all()
    if request.method == "GET":
        return render(request, "orders/all_products.html", {"objects" : objects, "session_set" : False})
    elif request.method == "POST":
        request.session['cart'] = create_session_dict(request.POST.dict())
        request.session.save()
        return redirect('checkout')


@login_required
def checkout(request):
    report = generate_transaction_report(dealer_name=request.user.username, session_cart=request.session["cart"])
    if report is None:
        return render(request, "custom_templates/page-500.html")

    if request.method == "GET":
        return render(request, "orders/checkout_page.html", {"report" : report})
    elif request.method == "POST":
        return render(request, "orders/checkout_page.html", {"success" : True, "report" : report})


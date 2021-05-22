from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_management.support import is_employee
from order_management.models import Product
from order_management.support import create_session_dict, generate_transaction_report, save_transaction
from core.template_declarations import *
import json


def test(request):
    print(request)
    return render(request, HOME)


@login_required
def add_product(request):
    if not is_employee(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        return render(request, ORDER_ADD_PRODUCT)
    elif request.method == "POST":
        product_data = request.POST.dict()
        try:
            try:
                float(product_data['price'])
            except Exception as e:
                return render(request, ORDER_ADD_PRODUCT, {"msg": "price should be in numbers"})
            product_obj = Product.objects.create(
                type=product_data['type'], name=product_data['name'], price=float(product_data['price']), uom=product_data['uom'])
            product_obj.full_clean()
            product_obj.save()
        except Exception as error_set:
            print("Error: ", error_set)
            err_response = ""
            for error in error_set:
                err_response += error[0] + " : " + error[1][0] + "</br>"
            return render(request, ORDER_ADD_PRODUCT, {"msg": err_response})
        else:
            msg = "Product {} added".format(product_data['name'])
            return render(request, ORDER_ADD_PRODUCT, {"msg": msg})


@login_required
def add_products_from_csv(request):
    pass


@login_required
def add_item_to_cart(request):
    objects = Product.objects.all()
    if request.method == "GET":
        return render(request, ORDER_ALL_PRODUCTS, {"objects": objects, "session_set": False})
    elif request.method == "POST":
        request.session['cart'] = create_session_dict(request.POST.dict())
        request.session.save()
        return redirect('checkout')


@login_required
def checkout(request):
    # populate ORDER_CHECKOUT with report with some fields as editable like discount, etc
    # put a button to submit these editable fields which will go to POST
    if request.method == "GET":
        report = generate_transaction_report(
            dealer_username=request.user.username, session=request.session)
        if report is None:
            return render(request, ERROR_500)
        return render(request, ORDER_CHECKOUT, {"report": report})
    elif request.method == "POST":
        data = request.POST.dict()
        if save_transaction(data):
            return render(request, ORDER_CHECKOUT, {"success": True, "msg": "Order submitted. Thank you."})
        return render(request, 
                      ORDER_CHECKOUT, 
                      {"success": False, "msg": "Order cannot be submitted. Sorry for the inconvinience. Please try again later."}
                    )

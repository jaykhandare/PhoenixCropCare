from core.template_declarations import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from user_management.models import Dealer_Profile
from user_management.support import is_employee

from order_management.models import Product, Transaction
from order_management.support import (create_session_dict,
                                      generate_transaction_report,
                                      retrieve_report, save_transaction)


@login_required
def add_product(request):
    if not is_employee(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        return render(request, ORDER_ADD_PRODUCT)
    elif request.method == "POST":
        product_data = request.POST.dict()
        product_obj = None
        try:
            try:
                float(product_data['price'])
            except Exception as e:
                return render(request, ORDER_ADD_PRODUCT, {"msg": "price should be in numbers"})
            prod_id = product_data.get('id', False)
            if prod_id:
                try:
                    product_obj = Product.objects.get(id=prod_id)
                except Exception as e:
                    print(e)
                    return render(request, ERROR_500)
            else:
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
            msg = "Product {} added/modified".format(product_data['name'])
            return render(request, ORDER_ADD_PRODUCT, {"msg": msg})


@login_required
def edit_product(request):
    if request.method == "POST":
        if not is_employee(request):
            return render(request, ERROR_403)
        return add_product(request)
    elif request.method == "GET":
        try:
            product_obj = Product.objects.get(id=request.GET['product_id'])
        except Exception as e:
            print("Exception for retrieving Product at {}".format(__name__))
            print(e)
            return render(request, ERROR_500)
        return render(request, ORDER_ADD_PRODUCT, {"product": product_obj})


@login_required
def remove_product(request):
    if request.method == "POST":
        return render(request, ERROR_403)
    elif request.method == "GET":
        product_id = request.GET['product_id']
        try:
            prod_obj = Product.objects.get(id=product_id)
            prod_obj.delete()
        except Exception as e:
            print(e)
            return render(request, ERROR_404)
        return redirect('all_products')


@login_required
def add_products_from_csv(request):
    pass


def all_products(request):
    objects = Product.objects.all()
    if request.method == "GET":
        return render(request, ORDER_ALL_PRODUCTS, {"objects": objects, "is_staff": is_employee(request)})
    elif request.method == "POST":
        request.session['cart'] = create_session_dict(request.POST.dict())
        request.session.save()
        return redirect('checkout')


@login_required
def checkout(request):
    if request.method == "GET":
        report = generate_transaction_report(
            dealer_username=request.user.username, session_cart=request.session['cart'], type="CHECKOUT")
        if report is None:
            return render(request, ERROR_500)
        request.session['cart'] = None
        request.session.save()
        return render(request, ORDER_CHECKOUT, {"report": report})
    elif request.method == "POST":
        data = request.POST.dict()
        if save_transaction(data):
            request.session['cart'] = None
            request.session.save()
            return render(request, ORDER_CHECKOUT, {"success": True, "msg": "Order submitted. Thank you."})
        msg = "Order cannot be submitted. Sorry for the inconvinience. Please try again later."
        return render(request, ORDER_CHECKOUT, {"success": False, "msg": msg})


@login_required
def all_transactions(request, all_trans=None):
    internal_call = False
    if request.method == "GET":
        headers = ["actions", "invoice_number", "mode_of_transport", "total_pre_tax", "discount_percent",
                   "total_price_taxed", "payment_type", "is_accepted", "is_dispatched", "is_closed", "dateTime"]
        # this shows all transactions
        if is_employee(request) and all_trans is None:
            all_trans = Transaction.objects.all()
        # this shows transactions sent from a different call
        # mostly transactions of dealers under an employee
        elif all_trans is not None:
            internal_call = True
            headers.pop(0)
        # this shows transactions of a specific dealer to himself
        else:
            try:
                user_obj = User.objects.get(username=request.user.username)
                dealer_obj = Dealer_Profile.objects.get(
                    first_name=user_obj.first_name, last_name=user_obj.last_name)
                all_trans = Transaction.objects.filter(
                    customer_code=dealer_obj.code)
            except Exception as e:
                print(e)
                return render(request, ERROR_500)
        return render(request, ORDER_ALL_TRANS, {"is_staff": is_employee(request), "internal_call" : internal_call, "headers": headers, "transactions": all_trans})

    elif request.method == "POST":
        return render(request, ERROR_403)


@login_required
def view_transaction(request):
    if request.method == "GET":
        report = retrieve_report(
            dealer_username=request.user.username, invoice_number=request.GET['invoice_number'])
        if report is None:
            return render(request, ERROR_500)
        return render(request, ORDER_VIEW_TRANS, {"report": report})

    elif request.method == "POST":
        return render(request, ERROR_403)

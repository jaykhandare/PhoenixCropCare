"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from django.contrib.auth.models import User
from user_management.models import Dealer_Profile
from order_management.models import Product, Order, Transaction
from django.forms.models import model_to_dict

CGST = 5
SGST = 0
IGST = 0
ROUND_UP = 2


def create_session_dict(data):
    data.pop('csrfmiddlewaretoken')
    session_dict = {}
    for key, value in data.items():
        if "quantity" in key and value != '0':
            session_dict[key.replace("quantity", "")] = int(value)
    return session_dict


def generate_transaction_report(dealer_username=None, session_cart=None):
    # gathering dealer info
    trans_report = {}
    try:
        dealer_user_obj = User.objects.get(username=dealer_username)
    except Exception as e:
        print(e)
        return None
    first_name = dealer_user_obj.first_name
    last_name = dealer_user_obj.last_name

    try:
        dealer_obj = Dealer_Profile.objects.get(
            first_name=first_name, last_name=last_name)
    except Exception as e:
        print(e)
        return None
    dealer_profile = model_to_dict(dealer_obj)

    trans_report["dealer_profile"] = dealer_profile

    # setting transaction code in the database
    invoice_number = Transaction.objects.count() + 1
    trans_obj = Transaction.objects.create(
        invoice_number=invoice_number, customer_code=dealer_profile['code'])

    # processing session cart
    pre_tax_total = post_tax_total = 0
    for product_id, quantity in session_cart.items():
        product_obj = Product.objects.get(id=product_id)
        total_price_obj = round(product_obj.price * quantity, ROUND_UP)
        pre_tax_total += total_price_obj
        try:
            order_obj = Order.objects.create(invoice_number=invoice_number, product_code=product_obj.id,
                                             quntity=quantity, total_price=total_price_obj)
            order_obj.full_clean()
            order_obj.save()
        except Exception as e:
            print("Exceptions while creating order at {}".format(__name__))
            print(e)

    orders_details = []
    orders = Order.objects.filter(invoice_number=invoice_number)
    for order in orders:
        try:
            retrieved_product_obj = Product.objects.get(id=order.product_code)
        except Exception as e:
            print(e)
            raise ValueError("Undefined object being purchased")
        else:
            dict_this = {}
            dict_this["name"] = retrieved_product_obj.name
            dict_this["type"] = retrieved_product_obj.type
            dict_this["code"] = order.product_code
            dict_this["quantity"] = order.quntity
            dict_this["price"] = order.total_price
            dict_this["CGST"] = round(order.total_price * CGST / 100, ROUND_UP)
            dict_this["SGST"] = round(order.total_price * SGST / 100, ROUND_UP)
            dict_this["IGST"] = round(order.total_price * IGST / 100, ROUND_UP)
            dict_this["total_price"] = order.total_price + \
                dict_this["CGST"] + dict_this["SGST"] + dict_this["IGST"]
            dict_this["total_price"] = round(
                dict_this["total_price"], ROUND_UP)
            post_tax_total += dict_this["total_price"]
            orders_details.append(dict_this)
    trans_report["orders_details"] = orders_details

    trans_obj.total_pre_tax = round(pre_tax_total, ROUND_UP)
    trans_obj.total_price_taxed = round(post_tax_total, ROUND_UP)
    try:
        trans_obj.full_clean()
        trans_obj.save()
    except Exception as e:
        print("Exceptions while saving transaction at {}".format(__name__))
        print(e)

    trans_details = model_to_dict(trans_obj)
    trans_report["trans_details"] = trans_details

    return trans_report

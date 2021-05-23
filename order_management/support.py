"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from django.contrib.auth.models import User
from user_management.models import Dealer_Profile
from order_management.models import Product, Order, Transaction
from django.forms.models import model_to_dict
from ast import literal_eval


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


def generate_transaction_report(dealer_username=None, session=None):
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

    # processing session cart
    pre_tax_total = post_tax_total = 0
    orders_details = []

    if session['cart'] is None:
        return None
    for product_id, quantity in session['cart'].items():
        product_obj = Product.objects.get(id=product_id)
        price = round(product_obj.price * quantity, ROUND_UP)
        pre_tax_total += price
        dict_this = {}
        dict_this["name"] = product_obj.name
        dict_this["type"] = product_obj.type
        dict_this["code"] = product_id
        dict_this["quantity"] = quantity
        dict_this["price"] = price
        dict_this["CGST"] = round(price * CGST / 100, ROUND_UP)
        dict_this["SGST"] = round(price * SGST / 100, ROUND_UP)
        dict_this["IGST"] = round(price * IGST / 100, ROUND_UP)
        dict_this["total_price"] = price + \
            dict_this["CGST"] + dict_this["SGST"] + dict_this["IGST"]
        dict_this["total_price"] = round(
            dict_this["total_price"], ROUND_UP)
        post_tax_total += dict_this["total_price"]
        orders_details.append(dict_this)

    trans_report["orders_details"] = orders_details

    trans_details = {}
    trans_details['total_pre_tax'] = round(pre_tax_total, ROUND_UP)
    trans_details['total_price_taxed'] = round(post_tax_total, ROUND_UP)
    trans_report["trans_details"] = trans_details

    session['cart'] = None

    return trans_report


def save_transaction(data=None):
    if data is None:
        print("no data provided in {}".format(__name__))
        return False

    report = literal_eval(data['report'])
    if "<class 'dict'>" != str(type(report)):
        print("invalid data in {}".format(__name__))
        return False

    dealer_code = report['dealer_code']
    mode_of_transport = data['mode_of_transport']
    payment_type = data['payment_type']
    orders = report['orders_details']
    transaction = report['trans_details']

    # add transaction
    try:
        transaction_count = Transaction.objects.count() + 1
        trans_obj = Transaction.objects.create(
            invoice_number=transaction_count,
            customer_code=dealer_code,
            mode_of_transport=mode_of_transport,
            total_pre_tax=transaction['total_pre_tax'],
            total_price_taxed=transaction['total_price_taxed'],
            payment_type=payment_type,
            is_accepted=True)
        trans_obj.full_clean()
        trans_obj.save()
    except Exception as e:
        print(e)
        return False

    # add orders
    for order in orders:
        try:
            order_obj = Order.objects.create(invoice_number=transaction_count, product_code=order['code'], quantity=order['quantity'], total_price=order['price'])
            order_obj.full_clean()
            order_obj.save()
        except Exception as e:
            trans_obj.delete()
            order_obj.delete()
            print(e)
            return False
    
    return True

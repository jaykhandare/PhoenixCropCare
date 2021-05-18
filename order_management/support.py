"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from django.contrib.auth.models import User
from user_management.models import Dealer_Profile
from order_management.models import Product, Order, Transaction
from django.forms.models import model_to_dict


def generate_transaction_report(dealer_username=None, session_cart=None):
    # retrieve dealer name from User
    # retrieve dealerProfile with dealer name
    # retrieve prices of various items from Product
    # create a unique transaction code
    # add transcode and products in order
    # generate total and other fields and put it into transaction
    # generate report and send back

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
    grand_total = 0
    for product_id, quantity in session_cart.items():
        product_obj = Product.objects.get(id=product_id)
        total_price_obj = product_obj.price * quantity
        grand_total += total_price_obj
        try:
            order_obj = Order.objects.create(invoice_number=invoice_number, product_code=product_obj.id,
                                             quntity=quantity, uom="pieces", total_price=total_price_obj)
            order_obj.full_clean()
            order_obj.save()
        except Exception as e:
            print("Exceptions while creating order at {}".format(__name__))
            print(e)

    trans_obj.total_pre_tax = round(grand_total, 3)
    try:
        trans_obj.full_clean()
        trans_obj.save()
    except Exception as e:
        print("Exceptions while saving transaction at {}".format(__name__))
        print(e)

    trans_details = model_to_dict(trans_obj)
    trans_report["trans_details"] = trans_details

    return trans_report


def create_session_dict(data):
    data.pop('csrfmiddlewaretoken')
    session_dict = {}
    for key, value in data.items():
        if "quantity" in key and value != '0':
            session_dict[key.replace("quantity", "")] = int(value)
    return session_dict

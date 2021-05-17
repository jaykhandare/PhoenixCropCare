"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from django.contrib.auth.models import User
from user_management.models import Dealer_Profile
from order_management.models import Product, Order, Transaction



def generate_transaction_report(dealer_name=None, session_cart=None):
    # returns None in case of error
    print(dealer_name)
    print(session_cart)
    return session_cart

def create_session_dict(data):
    data.pop('csrfmiddlewaretoken')
    session_dict = {}
    for key, value in data.items():
        if "quantity" in key and value != '0':
            session_dict[key.replace("quantity", "")] = int(value)
    return session_dict



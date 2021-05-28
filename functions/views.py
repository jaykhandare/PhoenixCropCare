from order_management.models import Transaction
from core.template_declarations import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from user_management.models import Dealer_Profile
from user_management.support import is_employee
from user_management.views import all_dealers
from order_management.views import all_transactions

from functions.models import Taxes
from functions.support import get_taxes_objects


def home_view(request):
    return render(request, FUNCTIONS_HOME)


@login_required
def get_my_dealers(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "POST":
        return render(request, ERROR_404)

    username = request.user.username
    try:
        dealers = Dealer_Profile.objects.filter(managed_by=username)
    except Exception as e:
        print(e)
        return render(request, ERROR_500)
    else:
        print("{} dealers found for {}".format(len(dealers), username))
        return all_dealers(request, internal_call=True, data=dealers)


@login_required
def modify_tax_rates(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    taxes = get_taxes_objects()
    if request.method == "GET":
        return render(request, FUNCTIONS_TAX_MODIFY, {"taxes": taxes})
    elif request.method == "POST":
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        for id, rate in data.items():
            if float(rate) > 100:
                return render(request, FUNCTIONS_TAX_MODIFY, {"taxes": taxes, "msg": "tax cannot be more than 100 for"})
            try:
                tax_obj = Taxes.objects.get(id=id)
                tax_obj.rate = rate
                tax_obj.full_clean()
                tax_obj.save()
            except Exception as e:
                print(e)
                return render(request, ERROR_500)
        taxes = get_taxes_objects()
        return render(request, FUNCTIONS_TAX_MODIFY, {"taxes": taxes, "msg": "Taxes updated"})


@login_required
def get_my_sales(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "POST":
        return render(request, ERROR_404)
    username = request.user.username
    all_trans = []
    try:
        dealers = Dealer_Profile.objects.filter(managed_by=username)
        for dealer in dealers:
            trans = Transaction.objects.filter(customer_code=dealer.code)
            all_trans.extend(trans)
    except Exception as e:
        print(e)
        return render(request, ERROR_500)

    return all_transactions(request, all_trans)


@login_required
def employee_performance(request):
    # this function will return a aggregated view of work done by employees
    # this will include the dealers acquired and total cash inflow from them
    # can be later modified to add other parameters
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "POST":
        return render(request, ERROR_404)

    return render(request, FUNCTIONS_HOME)


@login_required
def management(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "GET":
        # this would be easier if all these links are simply put in HTML itself
        # but we are putting it here to make it more dynamic so that we don't need to modify HTML
        labels = ("All Users", "Add Employee", "Remove Employee", "Edit Employee Details",
                  "All Dealers", "Add Dealer", "Remove Dealer", "Edi Dealer Details",
                  "All Products", "Add New Product", "Edit Product Details", "Remove a Product", 
                  "All Transactions", "View a Transaction",
                  "Tax Rates Modification", "Employee Performance",
                  )
        links = []
        return render(request, FUNCTIONS_MNGT_TASK, {"labels": labels, "links": links})
    elif request.method == "POST":
        return render(request, ERROR_404)

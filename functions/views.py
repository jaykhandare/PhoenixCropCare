from core.template_declarations import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from user_management.models import Dealer_Profile
from user_management.support import is_employee
from user_management.views import all_dealers

from functions.models import Taxes
from functions.support import get_taxes_objects


@login_required
def home_view(request):
    return render(request, HOME)


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
        return render(request, TAX_MODIFICATION, {"taxes": taxes})
    elif request.method == "POST":
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        for id, rate in data.items():
            if float(rate) > 100:
                return render(request, TAX_MODIFICATION, {"taxes": taxes, "msg": "tax cannot be more than 100 for"})
            try:
                tax_obj = Taxes.objects.get(id=id)
                tax_obj.rate = rate
                tax_obj.full_clean()
                tax_obj.save()
            except Exception as e:
                print(e)
                return render(request, ERROR_500)
        taxes = get_taxes_objects()
        return render(request, TAX_MODIFICATION, {"taxes": taxes, "msg": "Taxes updated"})


@login_required
def get_my_sales(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "POST":
        return render(request, ERROR_404)

    username = request.user.username

    return render(request, HOME)


@login_required
def get_total_sales(request):
    if not is_employee(request):
        return render(request, ERROR_403)
    if request.method == "POST":
        return render(request, ERROR_404)

    return render(request, HOME)


def get_sales_rep_near_me(request):
    if request.method == "POST":
        return render(request, ERROR_404)

    taluka = request.GET['taluka']
    district = request.GET['district']

    return render(request, HOME)

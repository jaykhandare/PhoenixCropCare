from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from user_management.support import is_staff
from user_management.models import Dealer_Profile
from user_management.views import all_dealers

@login_required
def home_view(request):
    return render(request, "custom_templates/home.html")


@login_required
def get_my_dealers(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    username = request.user.username
    try:
        dealers = Dealer_Profile.objects.filter(managed_by=username)
    except Exception as e:
        print(e)
        return render(request, "custom_templates/page-500.html")
    else:
        print("{} dealers found for {}".format(len(dealers), username))
        return all_dealers(request, internal_call=True, data=dealers)


@login_required
def get_my_sales(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    username = request.user.username

    return render(request, "custom_templates/home.html")


@login_required
def get_total_sales(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    username = request.user.username

    return render(request, "custom_templates/home.html")


@login_required
def get_my_position_hierarchy(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    username = request.user.username

    return render(request, "custom_templates/home.html")


def get_products(request):
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    return render(request, "custom_templates/home.html")


def get_offers(request):
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    return render(request, "custom_templates/home.html")


def get_sales_rep_near_me(request):
    if request.method == "POST":
        return render(request, "custom_templates/page-404.html")

    taluka = request.GET['taluka']
    district = request.GET['district']

    return render(request, "custom_templates/home.html")
from django.shortcuts import render
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PIL import Image
from os import path

from user_management.support import *
from user_management.forms import DealerDeleteForm
from user_management.models import Dealer_Profile, User_Profile, DeletedDealers
from core.settings import MEDIA_ROOT


@login_required
def all_users(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")

    if request.method == "GET":
        # fill this data with data of all users and then modify the tables-simple.html
        all_users_data = User.objects.all()
        headers = ["Username", "First Name", "Last Name",
                   "Email", "Last Active", "Actions for account", ]
        return render(request, "custom_templates/tables-simple.html", {"data": all_users_data, "headers": headers, "type": "users"})
    else:
        return render(request, "custom_templates/page-404.html")


@login_required
def all_dealers(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")

    if request.method == "GET":
        # fill this data with data of all dealers and then modify the tables-simple.html
        all_dealers_data = Dealer_Profile.objects.all()
        headers = ["Code", "First Name", "Last Name", "Firm Name",
                   "Contact", "Managed By", "Authorized", "Actions for account"]
        return render(request, "custom_templates/tables-simple.html", {"data": all_dealers_data, "headers": headers, "type": "dealers"})
    else:
        return render(request, "custom_templates/page-404.html")


@login_required
def profile(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")

    fs = FileSystemStorage()
    profile_picture_url = None

    if request.method == "GET":
        username = request.GET['username']
        try:
            profile_obj = User_Profile.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            data = model_to_dict(profile_obj)

            # remove not needed fields
            data.pop("id")
            data.pop("e_verified")

            # retrieve profile picture
            file_name = './users/' + username + '.png'
            if fs.exists(file_name):
                profile_picture_url = fs.url(file_name)
            else:
                profile_picture_url = fs.url('./users/profilePic.png')
            return render(request, "accounts/profile.html", {"data": data, "profile_picture": profile_picture_url})

    elif request.method == "POST":
        user_data = request.POST.dict()

        # processing profile picture
        try:
            uploaded_pic = request.FILES['profile_picture']
        except:
            pass
        else:
            file_name = './users/' + user_data['old_username'] + '.png'
            if fs.exists(file_name):
                print("replacing existing image")
                fs.delete(file_name)

            # store image using Pillow lib
            image = Image.open(uploaded_pic)
            image = image.resize((200, 300))
            path_to_storage = path.join(
                MEDIA_ROOT, "users/") + user_data['old_username'] + '.png'
            image.save(format="png", fp=path_to_storage)

        # processing data
        try:
            profile_obj = User_Profile.objects.get(
                username=user_data['old_username'])
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")

        profile_obj.username = user_data['username']
        profile_obj.address = user_data['address']
        profile_obj.city = user_data['city']
        profile_obj.taluka = user_data['taluka']
        profile_obj.district = user_data['district']
        profile_obj.state = user_data['state']
        profile_obj.pin_code = user_data['pin_code']
        profile_obj.contact = user_data['contact']
        profile_obj.position = user_data['position']
        profile_obj.manager = user_data['manager']
        profile_obj.authorized = user_data['authorized']

        try:
            profile_obj.save()
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            return render(request, "accounts/profile.html", {"msg": "Profile updated"})


@login_required
def register_dealer(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")

    if request.method == "GET":
        dealer_ordered_list = get_dealer_ordered_list(managed_by=request.user)
        return render(request, "dealers/basic_form.html", {"data": dealer_ordered_list, "type": "register"})
    elif request.method == "POST":
        dealer_data = request.POST.dict()
        return save_data_and_respond(request=request, data=dealer_data, processing_type="ADD")


@login_required
def edit_dealer(request):
    if not is_staff(request):
        return render(request, "custom_templates/unauthorized_access.html")

    if request.method == "GET":
        firm_name = request.GET['firm_name']
        data = get_dealer_ordered_list(firm_name=firm_name)
        if data is None:
            return render(request, "custom_templates/page-404.html")
        return render(request, "dealers/basic_form.html", {"data": data, "type": "edit"})

    elif request.method == "POST":
        dealer_data = request.POST.dict()
        return save_data_and_respond(request=request, data=dealer_data, processing_type="EDIT")


@login_required
def remove_dealer(request):
    if request.method == "GET":
        form = DealerDeleteForm()
        return render(request, "dealers/delete_form.html", {"form": form})
    elif request.method == "POST":
        dealer = request.POST.dict()

        try:
            retrieved_dealer = Dealer_Profile.objects.get(
                code=dealer['code'], managed_by=dealer['managed_by'])
        except Exception as e:
            # this means dealer is not there in the db,
            # still that's okay, reply with a basic error saying dealer not registered
            # send a correct message later on
            return render(request, "custom_templates/page-404.html")
        try:
            save_deleted_dealer(retrieved_dealer)
            retrieved_dealer.delete()
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")

        # reply with a success message
        return render(request, "custom_templates/page-404.html")


def testFunction(request):
    print("TEST")
    return render(request, "custom_templates/page-500.html")


def save_deleted_dealer(dealer=None):
    if dealer is not None:
        try:
            DeletedDealers.objects.create(
                first_name=dealer.first_name,
                last_name=dealer.last_name,
                firm_name=dealer.firm_name,
                managed_by=dealer.managed_by,
                address=dealer.address,
                city=dealer.city,
                pin_code=dealer.pin_code,
                contact=dealer.contact,
                email=dealer.email
            )
        except Exception as e:
            print(e)

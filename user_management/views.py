from django.shortcuts import render
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PIL import Image
from os import path

from user_management.models import Dealer_Profile, User_Profile
from core.settings import DEBUG, MEDIA_ROOT


@login_required
def all_users(request):
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
    if request.method == "GET":
        # fill this data with data of all dealers and then modify the tables-simple.html
        all_dealers_data = Dealer_Profile.objects.all()
        headers = ["Code", "First Name", "Last Name", "Firm Name",
                   "Contact", "Managed By", "Actions for account"]
        return render(request, "custom_templates/tables-simple.html", {"data": all_dealers_data, "headers": headers, "type": "dealers"})
    else:
        return render(request, "custom_templates/page-404.html")


def initiate_user_profile(username):
    profile_obj = User_Profile(username=username)
    try:
        profile_obj.save()
    except Exception as e:
        print(e)
        return False
    else:
        print("user profile added: {}".format(username))
        return True


@login_required
def profile(request):
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
        try:
            uploaded_pic = request.FILES['profile_picture']
        except:
            pass
        else:
            file_name = './users/' + user_data['old_username'] + '.png'
            if fs.exists(file_name):
                print("replacing existing image")
                fs.delete(file_name)

            # store image using PIL.Image
            image = Image.open(uploaded_pic)
            image = image.resize((200, 300))
            path_to_storage = path.join(
                MEDIA_ROOT, "users/") + user_data['old_username'] + '.png'
            image.save(format="png", fp=path_to_storage)

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


def get_dealer_ordered_list(managed_by, dealer_obj=None):
    if dealer_obj is None:
        ordered_list = [['code', ""], ['auth_number', ""], ['first_name', ""], ['last_name', ""], ['firm_name', ""], ['pd_open_date', ""], ['address', ""], ['city', ""], ['taluka', ""], ['district', ""], ['state', ""], ['pin_code', ""], ['contact', ""], ['email', ""], ['pan_number', ""], ['GST_number', ""], [
            'seed_license', ""], ['pesticide_license', ""], ['fertilizer_license', ""], ['SD_receipt_code', ""], ['SD_expected', ""], ['SD_deposited', ""], ['SD_receipt_date', ""], ['SD_payment_type', ""], ['exp_first_order', ""], ['managed_by', managed_by], ['agreement_done', ""], ['gift_sent', ""], ['authorized', ""]]
        return ordered_list


@login_required
def register_dealer(request):
    if request.method == "GET":
        orlist = get_dealer_ordered_list(managed_by=request.user)
        return render(request, "dealers/register_dealer.html", {"data": orlist})
    elif request.method == "POST":
        dealer_data = request.POST.dict()
        dealer_obj = Dealer_Profile(
            code=dealer_data['code'],
            auth_number=dealer_data['auth_number'],
            first_name=dealer_data['first_name'],
            last_name=dealer_data['last_name'],
            firm_name=dealer_data['firm_name'],
            pd_open_date=dealer_data['pd_open_date'],
            address=dealer_data['address'],
            city=dealer_data['city'],
            taluka=dealer_data['taluka'],
            district=dealer_data['district'],
            state=dealer_data['state'],
            pin_code=dealer_data['pin_code'],
            contact=dealer_data['contact'],
            email=dealer_data['email'],
            pan_number=dealer_data['pan_number'],
            GST_number=dealer_data['GST_number'],
            seed_license=dealer_data['seed_license'],
            pesticide_license=dealer_data['pesticide_license'],
            fertilizer_license=dealer_data['fertilizer_license'],
            SD_receipt_code=dealer_data['SD_receipt_code'],
            SD_expected=dealer_data['SD_expected'],
            SD_deposited=dealer_data['SD_deposited'],
            SD_receipt_date=dealer_data['SD_receipt_date'],
            SD_payment_type=dealer_data['SD_payment_type'],
            exp_first_order=dealer_data['exp_first_order'],
            managed_by=dealer_data['managed_by'],
            agreement_done=dealer_data['agreement_done'],
            gift_sent=dealer_data['gift_sent'],
            authorized=dealer_data['authorized']
        )
        try:
            dealer_obj.save()
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            return render(request, "dealers/register_dealer.html", {"msg": "Dealer registered"})


@login_required
def edit_dealer(request):
    if request.method == "GET":
        return render(request, "custom_templates/tables-simple.html")
    else:
        return render(request, "custom_templates/page-404.html")


@login_required
def remove_dealer(request):
    if request.method == "GET":
        return render(request, "custom_templates/tables-simple.html")
    else:
        return render(request, "custom_templates/page-404.html")

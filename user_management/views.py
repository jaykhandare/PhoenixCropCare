from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from core.settings import MEDIA_ROOT
from PIL import Image
from os import path

from user_management.forms import DealerDeleteForm, UserDeleteForm
from user_management.models import Dealer_Profile, User_Profile
from user_management.support import *
from core.template_declarations import *


@login_required
def all_users(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        all_users_data = User.objects.all()
        headers = ["Username", "First Name", "Last Name",
                   "Email", "Last Active", "Actions for account", ]
        return render(request, PROFILE_TABLE, {"data": all_users_data, "headers": headers, "type": "users"})
    else:
        return render(request, ERROR_404)


@login_required
def all_dealers(request, internal_call=None, data=None):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        if internal_call is None:
            dealers_data = Dealer_Profile.objects.all()
        else:
            if data is None:
                return render(request, ERROR_500)
            else:
                dealers_data = data
        headers = ["Code", "First Name", "Last Name", "Firm Name",
                   "Contact", "Managed By", "Authorized", "Actions for account"]
        return render(request, PROFILE_TABLE, {"data": dealers_data, "headers": headers, "type": "dealers"})
    else:
        return render(request, ERROR_404)


@login_required
def remove_user(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        return render(request, USER_DELETE, {'form': UserDeleteForm})
    elif request.method == "POST":
        user_creds = request.POST.dict()
        try:
            user_obj = User.objects.get(
                username=user_creds['username'], email=user_creds['email'])
            user_obj.delete()
            user_profile = User_Profile.objects.get(
                username=user_creds['username'])
            user_profile.delete()
        except Exception as e:
            print(e)
            return render(request, ERROR_500)
        else:
            fs = FileSystemStorage()
            file_name = './users/' + user_creds['username'] + '.png'
            if fs.exists(file_name):
                fs.delete(file_name)
            return redirect('all_users')


@login_required
def profile(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    fs = FileSystemStorage()
    profile_picture_url = None

    if request.method == "GET":
        username = request.GET['username']
        try:
            profile_obj = User_Profile.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request, ERROR_500)
        else:
            data = model_to_dict(profile_obj)
            # remove not needed fields
            data.pop("id")
            data.pop("e_verified")
            # date fields are not handled correctly by model to dict
            data['date_of_birth'] = profile_obj.date_of_birth
            data['date_of_joining'] = profile_obj.date_of_joining

            file_name = './users/' + username + '.png'
            if fs.exists(file_name):
                profile_picture_url = fs.url(file_name)
            else:
                profile_picture_url = fs.url('./users/profilePic.png')
            return render(request, USER_PROFILE, {"data": data, "profile_picture": profile_picture_url})

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
            return render(request, ERROR_500)
        
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
            profile_obj.full_clean()
            profile_obj.save()
        except Exception as error_set:
            err_response = ""
            for error in error_set:
                err_response += error[0] + " : " + error[1][0] + "</br>"
            
            file_name = './users/' + user_data['old_username'] + '.png'
            if fs.exists(file_name):
                profile_picture_url = fs.url(file_name)
            else:
                profile_picture_url = fs.url('./users/profilePic.png')

            user_data.pop('csrfmiddlewaretoken')
            user_data.pop('old_username')
            user_data.pop('profile_picture')
            return render(request, USER_PROFILE, {"msg": err_response, "data": user_data, "profile_picture": profile_picture_url})
        else:
            return render(request, USER_PROFILE, {"msg": "Profile updated"})


@login_required
def register_dealer(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        dealer_ordered_list = get_dealer_ordered_list(managed_by=request.user)
        return render(request, DEALER_REG_EDIT, {"data": dealer_ordered_list, "type": "register"})
    elif request.method == "POST":
        dealer_data = request.POST.dict()
        return save_data_and_respond(request=request, data=dealer_data, processing_type="ADD")


@login_required
def edit_dealer(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        firm_name = request.GET['firm_name']
        dealer_data = get_dealer_ordered_list(firm_name=firm_name)
        if dealer_data is None:
            return render(request, ERROR_404)
        return render(request, DEALER_REG_EDIT, {"data": dealer_data, "type": "edit"})
    elif request.method == "POST":
        dealer_data = request.POST.dict()
        return save_data_and_respond(request=request, data=dealer_data, processing_type="EDIT")


@login_required
def remove_dealer(request):
    if not is_staff(request):
        return render(request, ERROR_403)

    if request.method == "GET":
        form = DealerDeleteForm()
        return render(request, DEALER_DELETE, {"form": form})
    elif request.method == "POST":
        dealer = request.POST.dict()
        try:
            retrieved_dealer = Dealer_Profile.objects.get(
                code=dealer['code'], managed_by=dealer['managed_by'])
            username = retrieved_dealer.first_name.lower()[0] + retrieved_dealer.last_name.lower() + "404"
            user_obj = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request, ERROR_404)
        else:
            user_obj.delete()
            retrieved_dealer.delete()
        return redirect('all_dealers')

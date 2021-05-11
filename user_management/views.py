from django.shortcuts import render
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from user_management.models import UserProfile
from core.settings import DEBUG


@login_required
def all_users(request):
    if request.method == "GET":
        # fill this data with data of all users and then modify the tables-simple.html
        all_users_data = User.objects.all()
        data = all_users_data
        return render(request, "custom_templates/tables-simple.html", {"data": data})

    else:
        return render(request, "custom_templates/page-404.html")


def initiate_user_profile(username):
    profile_obj = UserProfile(username=username)
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
    if request.method == "GET":
        username = request.GET['username']
        try:
            profile_obj = UserProfile.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request, "custom_templates/page-500.html")
        else:
            data = model_to_dict(profile_obj)
            # remove not needed fields
            data.pop("id")
            data.pop("e_verified")
            return render(request, "custom_templates/profile.html", {"data": data})
    elif request.method == "POST":
        user_data = request.POST.dict()
        if request.FILES['profile_picture']:
            print(request.FILES['profile_picture'])
        else:
            print("file not found")
        try:
            profile_obj = UserProfile.objects.get(
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
            return render(request, "custom_templates/profile.html", {"msg": "Profile updated"})

from random import randint

from core.settings import DEBUG
from core.template_declarations import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from functions.views import home_view
from user_management.models import User_Profile

from authentication.forms import LoginForm, SignUpForm


def register_user(request):
    msg = None
    success = False

    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(e)
                return render(request, ERROR_404)

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            try:
                usr_obj = User.objects.get(
                    first_name=first_name, last_name=last_name, username="")
            except Exception as e:
                msg = 'User cannot be created. Exception : {}'.format(str(e))
                print(msg)
                return render(request, ERROR_500)
            else:
                username = ""
                if DEBUG:
                    # decide on username as auser for Axel User
                    username = form.cleaned_data.get("first_name").lower(
                    )[0] + form.cleaned_data.get("last_name").lower()
                else:
                    # this means we have to setup a temporary username
                    username = str(randint(1, 1000))

                usr_obj.username = username
                try:
                    usr_obj.save()
                    User_Profile.objects.create(username=username)
                except Exception as e:
                    print(e)
                    return render(request, ERROR_500)

                if DEBUG:
                    user = authenticate(
                        username=username, password=form.cleaned_data.get("password1"))
                    login(request, user)
                    return redirect("login")

                msg = 'User created {}- please provide documentation for verification'.format(
                    usr_obj.username)
                success = True
        else:
            msg = 'Form is not valid'

    return render(request, USER_REGISTER, {"form": form, "msg": msg, "success": success})


def login_view(request):
    msg = None

    if request.method == "GET":
        if request.user.is_authenticated:
            return home_view(request)
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, USER_LOGIN, {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return render(request, USER_LOGOUT)

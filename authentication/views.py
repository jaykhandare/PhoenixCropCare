from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from random import randint
from core.settings import DEBUG

from user_management.views import initiate_user_profile


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
                return render(request, "custom_templates/page-404.html")

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            try:
                usr_obj = User.objects.get(
                    first_name=first_name, last_name=last_name, username="")
            except Exception as e:
                msg = 'User cannot be created. Exception : {}'.format(str(e))
                print(e)
                return render(request, "custom_templates/page-500.html")
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
                except Exception as e:
                    print(e)
                    return render(request, "custom_templates/page-500.html")

                # add an empty entry in profile table
                is_initiated = initiate_user_profile(username=username)
                if not is_initiated:
                    return render(request, "custom_templates/page-500.html")

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

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def login_view(request):
    msg = None

    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if DEBUG:
                    return redirect("login")
                else:
                    # redirect to user homepage later
                    return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return render(request, "accounts/logout.html")

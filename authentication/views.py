from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User

from core.settings import DEBUG
from random import randint

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if DEBUG:
                    return redirect("login")
                else:
                    return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):
    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            try:
                usr_obj = User.objects.get(first_name=first_name, last_name=last_name, username="")
            except Exception as e:
                print(e)
            else:
                if DEBUG:
                    # decide on username as auser for Axel User
                    username = form.cleaned_data.get("first_name").lower()[0] + form.cleaned_data.get("last_name").lower()
                    usr_obj.username = username
                    usr_obj.save()
                    user = authenticate(username=username, password=form.cleaned_data.get("password1"))
                    login(request, user)
                    return redirect("login")
                else: 
                    # this means we have to setup a temporary username
                    usr_obj.username = str(randint(1,1000))
                    usr_obj.save()

            msg     = 'User created {}- please provide documentation for verification'.format(usr_obj.username)
            success = True

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


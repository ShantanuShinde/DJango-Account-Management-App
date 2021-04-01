from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import Context, loader
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

from .forms import *

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            ver_code = random.randint(1111, 9999)
            request.session["verification_code"] = ver_code
            request.session['username'] = username
            request.session['email'] = email
            request.session['password'] = password 
            email_html_temp = loader.get_template("verification_email.html")
            email_html = email_html_temp.render({'ver_code':ver_code, 'username':username})
            res = send_mail("Verification", '', from_email="djangoapp69@gmail.com", recipient_list=[email], html_message=email_html)
            
            return HttpResponseRedirect('/verification/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.create_user(request.session.get("username"), request.session.get("email"), request.session.get("password"))
            user.save()
            
            username = request.session.get("username")
            request.session.flush()
            request.session['username'] = username

            return HttpResponseRedirect('/ver_ack/')
    else:
        form = VerificationForm(request=request)
    return render(request, 'verification.html', {'form': form})

def verify_ack(request):
    return render(request, 'verification_ack.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data["username"]
            request.session['password'] = form.cleaned_data["password"]
            
            login(request, form.cleaned_data['user'])

            return HttpResponseRedirect('/main_page/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

@login_required
def main_page(request):
    images = ["1.jpg","2.jpg","3.jpg"]
    image = random.choice(images)

    return render(request, 'main_page.html', {'username': request.session.get('username'), "img":image})

def user_logout(request):
    request.session.flush()
    logout(request)

    return HttpResponseRedirect('/')

@login_required
def change_credenials(request):
    if request.method == "POST":
        if request.POST.get("username_bt"):
            form = ChangeUsername(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.session["username"])
                user.username = form.cleaned_data["username"]
                user.save()
                request.session["username"] = form.cleaned_data["username"]
                messages.info(request, "Username changed successfully")

                return HttpResponseRedirect("/main_page/")
            else:
                form1 = form
                form2 = ChangePassword(request=request)

        elif request.POST.get("password_bt"):
            form = ChangePassword(request.POST, request=request)
            if form.is_valid():
                form.cleaned_data["user"].set_password(form.cleaned_data["new_password"])
                form.cleaned_data["user"].save()
                messages.success(request, "Password changed successfully")
                request.session.flush()
                return HttpResponseRedirect("/login/")
            else:
                form1 = ChangeUsername()
                form2 = form
    else:
        form1 = ChangeUsername()
        form2 = ChangePassword(request=request)

    return render(request, 'change_credentials.html', {'form1':form1, 'form2':form2, 'username':request.session.get('username')})

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import Context, loader
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
import random

from .forms import *

def register(request):
    if request.method == 'POST':
        if request.POST.get('register'):
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
        elif request.POST.get('login'):
            return HttpResponseRedirect('/login/')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.create_user(request.session.get("name"), request.session.get("email"), request.session.get("password"))
            user.save()
            
            return HttpResponseRedirect('/ver_ack/')
    else:
        form = VerificationForm(request=request)
    return render(request, 'verification.html', {'form': form})

def verify_ack(request):
    return render(request, 'verification_ack.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data["username"]
            request.session['password'] = form.cleaned_data["password"]

            return HttpResponseRedirect('/main_page/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

def main_page(request):
    return render(request, 'main_page.html', {'username': request.session.get('username')})

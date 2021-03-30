from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import Context, loader
import random

from .forms import *

def register(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            ver_code = random.randint(1111, 9999)

            request.session["verification_code"] = ver_code

            email_html_temp = loader.get_template("verification_email.html")
            email_html = email_html_temp.render({'ver_code':ver_code})
            res = send_mail("Verification", '', from_email="djangoapp69@gmail.com", recipient_list=[email], html_message=email_html)
            
            return HttpResponseRedirect('/verification/')
    else:
        form = form = LoginForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            ver_code = request.session.get("verification_code")
            
            correct = ver_code == form.cleaned_data["verification_code"]

        return HttpResponse(str(correct))
    else:
        form = VerificationForm()
    return render(request, 'verification.html', {'form': form})
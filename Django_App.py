import os
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.template.loader import render_to_string
from login_form import LoginForm

DEBUG = True
SECRET_KEY = '_ro-(%nkd=(p8a_zp*d)d569d!^+y6--7=uh8#1+r04xns27!4'
ROOT_URLCONF = __name__
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': ['templates/']},]
EXTERNAL_APPS = [
  'django.contrib.staticfiles',
]
PROJECT_NAME = 'Django_App'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, PROJECT_NAME, 'staticfiles')
STATIC_URL = '/static/'

def home(request):
    html = render_to_string('home.html')
    return HttpResponse(html)

urlpatterns = [
    url(r'^$', home),
]
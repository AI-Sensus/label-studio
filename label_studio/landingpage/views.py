from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from rest_framework.authtoken.models import Token

# Create your views here.
def landingpageopen(request):
    return render(request, 'landingpage.html')

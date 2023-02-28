from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.say_hello, name = 'landingpage')
]
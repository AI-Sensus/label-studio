from django.urls import path
from . import views

app_name = 'subjectannotation'

urlpatterns = [
    path('', views.annotationtaskpage, name= 'annotationtaskpage'),
    path('create/', views.createannotationtask, name='create'),
    path('export/<int:project>',views.parse_subject_presence_annotations,name='export')
]

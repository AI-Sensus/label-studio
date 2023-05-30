from django.urls import path
from . import views

app_name = 'sensordata'

urlpatterns = [
    path('', views.sensordatapage, name= 'sensordatapage'),
    path('add/', views.addsensordata, name='add'),
    path('offset/', views.offset, name='offset'),
    path('parse/<str:file_path>/<int:sensor_model_id>', views.parse_sensor, name='parse_sensor'),

    path('offset/adjust/<int:id>/', views.adjust_offset, name='adjust_offset'),
    path('offset/delete/<int:id>', views.delete_offset, name='delete_offset'),
]
from django import forms
from sensormodel import models as sensormodelmodels


class SensorDataForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    sensor = forms.ModelChoiceField(sensormodelmodels.Sensor.objects.all())
    file = forms.FileField()

class SensorOffsetForm(forms.Form):
    sensor_1 = forms.ModelChoiceField(sensormodelmodels.Sensor.objects.all())
    sensor_2 = forms.ModelChoiceField(sensormodelmodels.Sensor.objects.all())
    offset = forms.IntegerField()
    offset_date = forms.DateTimeField()
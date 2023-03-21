from django import forms
from sensormodel.models import Sensor
from projects.models import Project

class SensorDataForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    sensor = forms.ModelChoiceField(Sensor.objects.all())
    project = forms.ModelChoiceField(Project.objects.all())
    file = forms.FileField()
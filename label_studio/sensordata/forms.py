from django import forms
from sensormodel.models import Sensor
from sensordata.models import SensorOffset, SensorData
from projects.models import Project

class SensorDataForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    sensor = forms.ModelChoiceField(Sensor.objects.all())
    file = forms.FileField()

class SensorOffsetForm(forms.ModelForm):
    class Meta:
        model = SensorOffset
        fields = ['sensor_A', 'sensor_B', 'offset', 'offset_Date']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Remove 'project' from kwarg
        super().__init__(*args, **kwargs)

        # Filter camera choices to show only sensors with sensortype 'C'
        if project:
            self.fields['sensor_A'].queryset = Sensor.objects.filter(project=project)

        # Filter imu choices to show only sensors with sensortype 'I'
        if project:
            self.fields['sensor_B'].queryset = Sensor.objects.filter(project=project)

class OffsetAnnotationForm(forms.Form):
    sync_sensordata = forms.ModelMultipleChoiceField(
        queryset=SensorData.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
     
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(OffsetAnnotationForm, self).__init__(*args, **kwargs)

        if project is not None:
            self.fields['sync_sensordata'].queryset = SensorData.objects.filter(project=project)
    
   

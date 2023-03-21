from django.db import models
from sensormodel.models import SensorType


class SensorData(models.Model):
    name = models.CharField(blank=True,null=True, max_length=100)
    project_id = models.IntegerField(blank=True,null=True)
    begin_datetime = models.DateTimeField(blank=True,null=True)
    end_datetime = models.DateTimeField(blank=True,null=True)
    file_hash = models.CharField(max_length=10,blank=True,null=True)
    sensortype = models.ForeignKey(SensorType,on_delete=models.CASCADE, null=True)
from django.db import models
from projects.models import Project

# Create your models here.
class MainProject(models.Model):
    name = models.CharField(max_length=50)
    project_id = models.IntegerField()

    def __str__(self):
        return 'Project: ' + self.name
    
class ZipFileModel(models.Model):
    zip_file = models.FileField(upload_to='zip_files/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Assuming Project is your existing model
    created_at = models.DateTimeField(auto_now_add=True)
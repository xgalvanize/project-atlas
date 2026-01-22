from django.db import models

# Create your models here.
from projects.models import Project

class Asset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to='assets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

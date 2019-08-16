import os

from django.db import models
from teacher.models import TeachersClassRoom
from datetime import datetime
from django.urls import reverse

from .utils import unique_slug_generator

class Assignment(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)
    instructions = models.CharField(max_length=100)
    due_date =  models.DateTimeField( blank=True, null = True)
    pub_date = models.DateTimeField(auto_now=True, null=True)
    classroom = models.ForeignKey(
        TeachersClassRoom, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)
        print(f"slud added {self.slug}")

    def get_files(self):
        files = AssignmentsFile.objects.filter(assignment=self)
        return files
    
    def __str__(self):
        return self.title



class AssignmentsFile(models.Model):
    file = models.FileField(upload_to='assignment/files/')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)
    
    def filename(self):
        return os.path.basename(self.file.name)

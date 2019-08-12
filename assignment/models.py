from django.db import models
from teacher.models import TeachersClassRoom
from datetime import datetime
from django.urls import reverse

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.CharField(max_length=100)
    due_date =  models.DateTimeField( blank=True, null = True)
    pub_date = models.DateField(auto_now=True, null=True)
    classroom = models.ForeignKey(
        TeachersClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class AssignmentsFile(models.Model):
    file = models.FileField(upload_to='assignment/files/')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

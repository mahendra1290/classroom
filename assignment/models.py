from django.db import models
from teacher.models import TeachersClassRoom
from datetime import datetime
from django.urls import reverse

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.CharField(max_length=100)
    due_date =  models.DateTimeField(default=datetime.now, blank=True, null = True)
    pub_date = models.DateField(auto_now=True, null=True)
    assignment_of_class = models.ForeignKey(
        TeachersClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('teacher:assignment_detail', args=[self.pk])


class AssignmentsFile(models.Model):
    file = models.FileField(upload_to='images/')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

from django.db import models
from customuser.models import User

class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
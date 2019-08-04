from django.db import models
from django.conf import settings

class Teacher(models.Model):
    name = models.CharField(max_length=20)
    teacher_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)


class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


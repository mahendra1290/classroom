from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=20)


class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


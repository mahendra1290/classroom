from django.db import models
from django.conf import settings

from django.urls import reverse

DEPARTMENT_CHOICES = (
    ('', 'Select Department'),
    ('CD', 'Computer Department'),
    ('EE', 'Electrical Department'),
    ('ECD', 'Electronics and Communication Department'),
    ('MD', 'Mechanical Department'),
    ('PD', 'Production and Industial Department'),
    ('CD', 'Civil Department'),
)

class Teacher(models.Model):
    teacher_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=20)
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, default='', blank=True)
    phone = models.IntegerField()

    def get_username(self):
        return self.teacher_user.email

    def __str__(self):
        return (self.name)


class TeachersClassRoom(models.Model):
    class_id = models.SlugField(max_length=10, unique=True)
    title = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=30)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('teacher:classroom_detail', args=[self.pk])

    def __str__(self):
        return self.title

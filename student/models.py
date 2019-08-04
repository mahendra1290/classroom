from django.db import models
from django.conf import settings

# Create your models here.
class Student(models.Model):
    student_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.student_user)



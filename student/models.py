from django.db import models
<<<<<<< HEAD
from django.conf import settings

# Create your models here.
class Student(models.Model):
    student_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.student_user)


=======

# Create your models here.
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d

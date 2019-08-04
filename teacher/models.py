from django.db import models

# Create your models here.
from user.models import User

class Teacher(User):
    phonenumber = models.CharField(null = True, blank = True, max_length = 10)
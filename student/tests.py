from django.test import TestCase
from django.contrib.auth.models import Group

from customuser.models import User
from .models import Student


def create_student(email, password):
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    user.is_active = True
    user.save()
    student = Student(
        name='student', 
        year='first_room',
        rollno=11812032,
        branch='computer engineering',
        user=user
    )
    student.save()
    return student


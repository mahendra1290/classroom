from django.test import TestCase
from customuser.models import User
from .models import Student

def create_student(email, password):
    base_user = User.objects.create_user(
        email=email,
        password=password,
    )
    base_user.save()
    student = Student(
        name='student', 
        year='first_room',
        rollno=11812032,
        branch='computer engineering',
        student_user = base_user
    )
    student.save()
    return student


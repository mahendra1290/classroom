from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=20)
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, default='', blank=True)
    phone = models.IntegerField()

    def get_username(self):
        return self.user.email
    
    def can_take_phone_number(self , new_phone_number:int)->bool:
        teacher = Teacher.objects.filter(phone=new_phone_number)
        if teacher.count() > 0 and teacher[0].phone is not self.phone:
            return False
        else:
            return True

    def update_name(self , new_name:str):
        self.name = new_name
        self.save()

    def update_department(self, new_department:str):
        self.department = new_department
        self.save()

    def update_phone_number(self, new_phone_number:int)->bool:
        self.phone = new_phone_number
        self.save()
    
    def __str__(self):
        return (self.name)

    class Meta:

        permissions = (
            ("can_create_classroom", 'can create a classroom'),
            ("can_create_assignment", '')
        )
    
    
class TeachersClassRoom(models.Model):
    class_id = models.SlugField(max_length=10, unique=True)
    title = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=30)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def set_class_id(self):
        while True:
            class_id = get_random_string(
                length=6, allowed_chars='abcdefghijklmnopqrstuv0123456789')
            classroom = TeachersClassRoom.objects.filter(class_id=class_id)
            if classroom.count() == 0:
                self.class_id = class_id
                break

    def get_absolute_url(self):
        return reverse('teacher:classroom_detail', args=[self.pk])

    def __str__(self):
        return self.title

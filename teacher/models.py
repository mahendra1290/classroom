from django.db import models
from django.conf import settings

from django.urls import reverse

from .utils import unique_slug_generator
from .utils import unique_class_id_generator
from phonenumber_field.modelfields import PhoneNumberField

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
    phone = PhoneNumberField(unique = True, null=True, blank = False, region = 'IN', max_length = 13) 

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
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=40)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def set_class_id(self):
        self.class_id = unique_class_id_generator(self)

    def save(self, *args, **kwargs):
        if self.class_id == "":
            self.set_class_id()
        self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs) 

    def belongs_to_teacher(self, user):
        teacher = self.teacher
        if teacher.user == user:
            return True
        return False

    def get_absolute_url(self):
        return reverse('teacher:classroom_detail', args=[self.pk])

    def __str__(self):
        return self.title

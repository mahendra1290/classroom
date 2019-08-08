from django.db import models
from django.contrib.auth.models import PermissionsMixin
from student.models import Student
from django.contrib.auth.models import Group

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime
from assignment.models import Assignment

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    teacher_status = models.BooleanField(default = False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    details = models.BooleanField(default=False) 
    USERNAME_FIELD = 'email'

    objects = UserManager()
    def __str__(self):
        return self.email

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def can_add_class(self):
        return self.teacher_status

    @property
    def can_add_assignment(self):
        return (not self.teacher_status)

    @property
    def is_teacher(self):
        return self.teacher_status

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_student(self):
        return not (self.teacher_status)
    
    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


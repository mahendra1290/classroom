from datetime import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group

from assignment.models import Assignment
from student.models import Student

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

    def create_user_for_teacher(self, email, password):
        user = self.create_user(email, password)
        try:
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
        except ObjectDoesNotExist:
            print("group not present")
        user.is_teacher = True
        user.save()
        return user
    
    def crate_user_for_student(self, email, password):
        user = self.create_user(email, password)
        try:
            group = Group.objects.get(name='student')
            user.groups.add(group)
        except ObjectDoesNotExist:
            print("group not present")
        user.save()
        return user

    def create_superuser(self,email,password):

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_teacher = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
   

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_in_groups(self, *group_names):
        if self.is_authenticated:
            if bool(self.groups.filter(name__in=group_names)) \
                or self.is_superuser:
                return True
        return False

    @property
    def is_student(self):
        return not self.is_teacher

    @property
    def is_staff(self):
        return self.is_admin


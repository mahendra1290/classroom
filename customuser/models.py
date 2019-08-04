from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime
from assignment.models import Assignment

class UserManager(BaseUserManager):
    def create_user_student(self, email,name ,year,branch,rollno,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError("Name Cannot Be left Blank")
        if not year:
            raise ValueError("Year Cannot Be left Blank")
        if not branch:
            raise ValueError("Branch must be selected")
        if not rollno:
            raise ValueError("RollNUmber must be filled")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            year = year,
            branch = branch,
            rollno = rollno,
        )

        user.set_password(password)
        user.save()
        user.is_teacher = False
        user.save(using=self._db)
        
        return user

    def create_superuser(self,email,name,password):
        user = self.model(
            name = name,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        user.is_teacher = True
        user.is_staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def create_user_teacher(self, email , name, password):
        user = self.model(
            email = self.normalize_email(email),
            name= name,
        )
        user.set_password(password)
        user.save()
        user.is_teacher = True
        user.save(using=self._db)
        return user

YEAR_CHOICES = (
    ('', 'Select Year'),
    ('firstyear','First Year'),
    ('secondyear','Second Year'),
    ('thirdyear','Third Year'),
    ('fourthyear','Fourth Year'),
)
BRANCH_CHOICES = (
    ('', 'Select Branch'),
    ('cse', 'Computer Engg.'),
    ('ee', 'Electrical Engg.'),
    ('ece', 'Electronics and Comm. Engg.'),
    ('me', 'Mechanical Engg.'),
    ('pie', 'Production and Industial Engg.'),
    ('ce', 'Civil Engg.'),

)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default='',blank=True, null = True)
    branch = models.CharField(max_length =50, choices = BRANCH_CHOICES, default ='',blank=True, null = True)
    name = models.CharField( max_length=50 , null = True, blank = False)
    rollno = models.CharField(max_length = 10, null=True, blank = False, unique = True)
    admin = models.BooleanField(default=False) # a superuser
    is_staff = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    myassignments = models.ManyToManyField(Assignment)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def get_username(self):
        return self.email

    def get_name(self):
        return self.name

    @property
    def is_admin(self):
        return self.admin

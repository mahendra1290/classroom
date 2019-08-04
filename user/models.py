from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import PermissionsMixin
from student.models import Student
=======
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime
from assignment.models import Assignment

class UserManager(BaseUserManager):
<<<<<<< HEAD
    def create_user(self, email,name ,year,branch,rollno,password=None):
=======
    def create_user_student(self, email,name ,year,branch,rollno,password=None):
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
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
<<<<<<< HEAD
        student_obj = Student()
        student_obj.student = user
        student_obj.save()
        return user

    def create_superuser(self,email,password):

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.staff = True
        user.admin = True
=======
        
        return user

    def create_superuser(self,email,name,password):

        user = self.model(
            email = self.normalize_email(email),
            name= name,
        )
        user.set_password(password)
        user.save()
        user.is_teacher = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def create_user_teacher(self, email , name, password):
        user = self.model(
            email = self.normalize_email(email),
            name= name,
        )
        user.set_password(password)
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
        user.save()
        user.is_teacher = True
        user.save(using=self._db)
        return user

<<<<<<< HEAD


=======
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
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

<<<<<<< HEAD
class User(AbstractBaseUser,PermissionsMixin):
=======
class User(AbstractBaseUser):
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default='',blank=True, null = True)
    branch = models.CharField(max_length =50, choices = BRANCH_CHOICES, default ='',blank=True, null = True)
    name = models.CharField( max_length=50 , null = True, blank = False)
    rollno = models.CharField(max_length = 10, null=True, blank = False, unique = True)
<<<<<<< HEAD
    is_teacher = models.BooleanField(default = False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
=======
    admin = models.BooleanField(default=False) # a superuser
    is_teacher = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
    myassignments = models.ManyToManyField(Assignment)
    USERNAME_FIELD = 'email'

    objects = UserManager()
<<<<<<< HEAD
    def __str__(self):
        if self.is_teacher is True:
            return self.email
        else :
            return self.rollno
=======
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d

    def get_username(self):
        # The user is identified by their email address
        return self.email

    def get_name(self):
        # The user is identified by their email address
        return self.name

<<<<<<< HEAD
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"

=======
    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d

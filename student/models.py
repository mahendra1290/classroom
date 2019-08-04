from django.db import models
from django.conf import settings
from assignment.models import Assignment
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

class Student(models.Model):
    student_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default='',blank=True, null = True)
    branch = models.CharField(max_length =50, choices = BRANCH_CHOICES, default ='',blank=True, null = True)
    name = models.CharField( max_length=50 , null = True, blank = False)
    rollno = models.CharField(max_length = 10, null=True, blank = False, unique = True)
    myassignments = models.ManyToManyField(Assignment, blank=True)

    def __str__(self):
        return str(self.student_user)


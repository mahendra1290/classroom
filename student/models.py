from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from assignment.models import Assignment
from teacher.models import TeachersClassRoom
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    year = models.CharField(max_length=50, choices=YEAR_CHOICES, default='',blank=True, null = True)
    branch = models.CharField(max_length =50, choices = BRANCH_CHOICES, default ='',blank=True, null = True)
    name = models.CharField( max_length=50 , null = True, blank = False)
    rollno = models.CharField(max_length = 10, null=True, blank = False, unique = True)
    my_classes = models.ManyToManyField(TeachersClassRoom, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        permissions = (
            ('can_add_solution' , 'can add solution to a assignment'),
            ('can_view_classroom', 'can view classroom page'),
            ('can_view_assignment', 'can view assignment'),
        )

    @classmethod
    def is_student_registered(cls, user):
        try:
            student = Student.objects.get(user=user)
            return True
        except ObjectDoesNotExist:
            return False
    @classmethod
    def get_student(cls, user):
        try:
            student = Student.objects.get(user=user)
            return student
        except ObjectDoesNotExist:
            return None


class Solution(models.Model):
    comment = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return ("submission of " + str(self.student))
    

class SolutionFile(models.Model):
    file = models.FileField(upload_to='submissions/')
    submission = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

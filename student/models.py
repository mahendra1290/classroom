from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from assignment.models import Assignment
from teacher.models import TeachersClassRoom

from django.core.validators import RegexValidator
from .utils import unique_slug_generator

import os

YEAR_CHOICES = (
    ('', 'Select Year'),
    ('firstyear', 'First Year'),
    ('secondyear', 'Second Year'),
    ('thirdyear', 'Third Year'),
    ('fourthyear', 'Fourth Year'),
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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    year = models.CharField(
        max_length=10, choices=YEAR_CHOICES, default='', blank=True, null=True)
    branch = models.CharField(
        max_length=30, choices=BRANCH_CHOICES, default='', blank=True, null=True)
    name = models.CharField(max_length=50, null=True, blank=False)
    rollno = models.CharField(validators=[RegexValidator(
        regex='^.{8}$', message='Length has to be 8', code='nomatch')],
        null=False, max_length=8, blank=False)
    my_classes = models.ManyToManyField(TeachersClassRoom, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        permissions = (
            ('can_add_solution', 'can add solution to a assignment'),
            ('can_view_classroom', 'can view classroom page'),
            ('can_view_assignment', 'can view assignment'),
        )
    
    def has_access_to_assignment(self, assignment):
        joined_classrooms = self.my_classes.all()
        classroom = assignment.classroom
        if classroom in joined_classrooms:
            return True
        return False

    def get_solution(self, assignment):
        if (self.has_access_to_assignment(assignment) 
                and self.has_submitted_solution(assignment)):
            solution = Solution.objects.filter(
                assignment=assignment, student=self)
            return solution.first()
        return None

    def has_submitted_solution(self, assignment):
        solution_exist = Solution.objects.filter(assignment=assignment, student=self).exists()
        if solution_exist:
            return True
        return False

    def can_get_rollnumber(self, new_rollnumber):
        student = Student.objects.filter(rollno=new_rollnumber)
        if student.count() == 0 or self.rollno == new_rollnumber:
            return True
        return False
    
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
    comment = models.CharField(max_length=150, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, unique=True)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def get_files(self):
        files = SolutionFile.objects.filter(submission=self)
        return files

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return ("submission of " + str(self.student))


class SolutionFile(models.Model):
    file = models.FileField(upload_to='submissions/')
    submission = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

    def filename(self):
        return os.path.basename(self.file.name)

from django.contrib import admin
from .models import Student
from .models import Solution
from .models import SolutionFile
from django.conf import settings


admin.site.register(Student)
admin.site.register(Solution)
admin.site.register(SolutionFile)

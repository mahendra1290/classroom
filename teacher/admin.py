from django.contrib import admin
from .models import Teacher
from django.conf import settings
from .models import TeachersClassRoom

admin.site.register(Teacher)
admin.site.register(TeachersClassRoom)

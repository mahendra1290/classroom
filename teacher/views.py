from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import FormView
from django.core.exceptions import ObjectDoesNotExist

from .models import TeachersClassRoom
from .models import Teacher
from assignment.models import Assignment
from .forms import ClassroomCreateForm
from student.models import Student

def is_class_id_used(class_id):
    try:
        classroom = TeachersClassRoom.objects.get(class_id=class_id)
        return True
    except ObjectDoesNotExist:
        return False

class ClassroomCreateView(LoginRequiredMixin, FormView):
    template_name = 'classroom_create.html'
    form_class = ClassroomCreateForm
    success_url = ''

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            title = form.cleaned_data['title']
            section = form.cleaned_data['section']
            subject = form.cleaned_data['subject']
            user = request.user
            teacher = Teacher.objects.get(user=user)
            while True:
                class_id = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuv0123456789')
                if not is_class_id_used(class_id):
                    break
            classroom = TeachersClassRoom(
                title=title, section=section, subject=subject, teacher=teacher, class_id=class_id)
            classroom.save()
            self.success_url = classroom.get_absolute_url()
            return self.form_valid(form)
        return self.form_invalid(form)


def home_page_view(request):
    try:
        teacher = Teacher.objects.get(user = request.user)
        queryset = TeachersClassRoom.objects.filter(teacher=teacher)
        context = {
            'teacher' : teacher,
            'classrooms' : queryset,
        }
        return render(request, 'teacher_window.html', context=context)
    except ObjectDoesNotExist:
        pass

@user_passes_test(must_be_a_teacher)
def classroom_detail_view(request, pk):
    classroom = TeachersClassRoom.objects.get(id=pk)
    student_list = classroom.student_set.all()
    assignment_query = Assignment.objects.filter(classroom=classroom)
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query
    }

    return render(request, 'classroom_detail.html', context)


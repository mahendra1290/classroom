from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TeachersClassRoom
from .models import Teacher
from assignment.models import Assignment, AssignmentsFile
from assignment.forms import AssignmentCreateForm
from .forms import ClassroomCreateForm
from django.urls import reverse
from django.http import HttpResponseRedirect
import student
from student import urls
import assignment


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
            base_user = request.user
            print(base_user)
            teacher = Teacher.objects.get(teacher_user=base_user)
            classroom = TeachersClassRoom(
                title=title, section=section, subject=subject, teacher=teacher)
            classroom.save()
            self.success_url = classroom.get_absolute_url()
            return self.form_valid(form)
        return self.form_invalid(form)


class HomePageListView(ListView):
    model = TeachersClassRoom
    template_name = 'teacher_window.html'
    context_object_name = 'classroom_list'

    def get_queryset(self):
        teacher = Teacher.objects.get(teacher_user=self.request.user)
        queryset = TeachersClassRoom.objects.filter(teacher=teacher)
        print(queryset)
        return queryset


def classroom_detail_view(request, pk):
    classroom = TeachersClassRoom.objects.get(id=pk)
    assignment_query = Assignment.objects.filter(assignment_of_class=classroom)
    print(assignment_query)
    print(classroom)
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query
    }
    return render(request, 'classroom_detail.html', context)


def add_assignment_view(request, pk):
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST)
        files = request.FILES.getlist('assign_file')
        if form.is_valid():
            classroom = TeachersClassRoom.objects.get(id=pk)
            assign = Assignment(
                title=form.cleaned_data['title'], 
                instructions=form.cleaned_data['instruction'],
                assignment_of_class=classroom
            )
            assign.save()
            for f in files:
                assignment_file = AssignmentsFile(file=f, assignment=assign)
                assignment_file.save()
            print(assign.get_absolute_url())
            return HttpResponseRedirect(str(assign.get_absolute_url()))
    else :
        form = AssignmentCreateForm()
    return render(request, 'index.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')


def delete_user(request):
    user_obj = User.objects.filter(email=request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')

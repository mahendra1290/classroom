from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login,logout
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
from .forms import ClassroomCreateForm
from django.urls import reverse
import student
from student import urls
import assignment

class ClassroomCreateView(LoginRequiredMixin , FormView):
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
            classroom = TeachersClassRoom(title=title, section=section, subject=subject, teacher=teacher)
            classroom.save()
            self.success_url = classroom.get_absolute_url()
            return self.form_valid(form)
        return self.form_invalid(form)

class ClassroomDetailView(DetailView):
    model = TeachersClassRoom
    context_object_name = 'classroom'
    template_name = 'classroom_detail.html'

class ClassroomListView(ListView):
    model = TeachersClassRoom
    template_name = 'classrooms.html'
    context_object_name = 'classroom_list'

    def get_queryset(self):
        teacher = Teacher.objects.get(teacher_user=self.request.user)
        queryset = TeachersClassRoom.objects.filter(teacher=teacher)
        print(queryset)
        return queryset
    

def classroom_detail_view(request, pk):
    classroom = TeachersClassRoom.objects.all()
    print(classroom[0].id)
    context = {
        'classroom' : classroom
    }
    return render(request, 'classroom_detail.html', context)

def HomePageViewTeacher(request):
    return render(request, 'home_teacher.html')


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.crypto import get_random_string

from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import FormView
from customuser.models import User
from .models import TeachersClassRoom
from .models import Teacher
from assignment.models import Assignment
from .forms import ClassroomCreateForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from customuser.forms import UserPasswordEditForm
from django.contrib.auth.models import Group
from student.models import Student
from .forms import TeacherEditForm

def must_be_a_teacher(user):
    if (user.is_authenticated):
        return user.is_teacher
    return False

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
        if queryset.count() is 0:
            count =0
        else :
            count = 1
        context = {
            'teacher' : teacher,
            'classrooms' : queryset,
            'count':count,
        }
        return render(request, 'teacher_window.html', context=context)
    except ObjectDoesNotExist:
        pass

@user_passes_test(must_be_a_teacher)
def classroom_detail_view(request, pk):
    print("HELLO WORLD")
    print(pk)
    classroom = TeachersClassRoom.objects.get(id=pk)
    print(classroom)
    student_list = classroom.student_set.all()
    assignment_query = Assignment.objects.filter(classroom=classroom)
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query
    }

    return render(request, 'classroom_detail.html', context)

def teacher_edit_view(request):
    teacher_obj = Teacher.objects.get(user= request.user)
    name = teacher_obj.name
    department = teacher_obj.department
    phone = teacher_obj.phone
    passwordEditForm = UserPasswordEditForm()
    teacherEditForm = TeacherEditForm()
    print(request.method)
    if request.method == 'POST':
        if 'teacheredit_submit' in request.POST:
            teacherEditForm = TeacherEditForm(request.POST)
            print(teacherEditForm)
            print(teacherEditForm.is_valid())
            if teacherEditForm.is_valid():
                teacher_obj.name = teacherEditForm.cleaned_data['name']
                teacher_obj.department = teacherEditForm.cleaned_data['department']
                new_phone = teacherEditForm.cleaned_data['phone']
                if new_phone!=phone:
                    phone_list = Teacher.objects.all()
                    print(phone_list)
                    for x in phone_list:
                        if new_phone == x.phone:
                            messages.error(request, 'Phone Number already exists.')
                            return render(request, 'teacher_editprofile.html', {'passwordEditForm': passwordEditForm, 'teacherEditForm':teacherEditForm})
                    teacher_obj.phone = new_phone
                try:
                    teacher_obj.save()
                    messages.success(request, 'Profile updated succesfully')
                except:
                    return render(request, 'teacher_editprofile.html', {'passwordEditForm': passwordEditForm, 'teacherEditForm':teacherEditForm,'teacher':teacher_obj})
                return redirect('teacher:teachers_homepage')
        else:
            teacherEditForm = TeacherEditForm(initial={'phone':phone, 'name':name , 'department':department})
            passwordEditForm = UserPasswordEditForm(request.POST)
            if passwordEditForm.is_valid():
                user_info = request.user
                email = user_info.email
                user_password = user_info.password
                old_password = passwordEditForm.cleaned_data['old_password']
                success = user_info.check_password(request.POST['old_password'])
                new_password = passwordEditForm.cleaned_data['new_password']
                confirm_password = passwordEditForm.cleaned_data['confirm_password']
                if not success:
                    messages.error(request, 'Current Password is not correct.')
                    return render(request, 'teacher_editprofile.html', {'passwordEditForm': passwordEditForm, 'teacherEditForm':teacherEditForm,' teacher':teacher_obj})
                if new_password!=confirm_password:
                    messages.error(request, 'Confirm Password doesnot match with New Password')
                    return render(request, 'teacher_editprofile.html', {'passwordEditForm': passwordEditForm, 'teacherEditForm':teacherEditForm,' teacher':teacher_obj})
                
                user_info.set_password(new_password)
                try:
                    user_info.save()
                    user = authenticate(request, username=email, password=new_password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Password is updated successfully')
                        return redirect('teacher:teachers_homepage')
                except:
                    return render(request, 'teacher_editprofile.html', {'passwordEditForm': passwordEditForm, 'teacherEditForm':teacherEditForm,' teacher':teacher_obj})
                return redirect('teacher:teachers_homepage')
                
    else:
        teacherEditForm = TeacherEditForm(initial={'phone':phone, 'name':name , 'department':department})
        passwordEditForm = UserPasswordEditForm()
    return render(request, 'teacher_editprofile.html', {'teacherEditForm': teacherEditForm, 'passwordEditForm': passwordEditForm,'teacher':teacher_obj})

def classroom_delete_view(request, pk):
    classroom = TeachersClassRoom.objects.get(id=pk)
    teacher_email = (classroom.teacher.user.email)
    if classroom is not None and request.user.email==teacher_email:
        classroom.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "Please enter a valid class Id")
    return redirect('teacher:teachers_homepage')

def classroom_edit_view(request,pk):
    form  = ClassroomCreateForm()
    classroom = TeachersClassRoom.objects.get(id=pk)
    url = reverse('teacher:classroom_detail', kwargs={'pk': pk})
    print(url)
    teacher_email = (classroom.teacher.user.email)
    if classroom is not None and request.user.email==teacher_email:
        if request.method =='POST':
            form  = ClassroomCreateForm(request.POST)
            if form.is_valid():
                classroom.title = form.cleaned_data['title']
                classroom.subject = form.cleaned_data['subject']
                classroom.section = form.cleaned_data['section']
                classroom.save()
                messages.success(request, "Classroom desctription has been updated")
                return redirect(url)
                
            else:
                messages.error(request, "Please enter valid details")

        
        else :
            form = ClassroomCreateForm(initial={'title':classroom.title, 'subject':classroom.subject, 'section':classroom.section})
            return render(request,'classroom_edit_view.html', {'form':form})

    else:
        messages.error(request, "Please enter a valid url")
        
    return HttpResponseRedirect(url)

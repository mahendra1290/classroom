from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

from .models import TeachersClassRoom
from .models import Teacher
from .forms import ClassroomCreateForm
from .forms import TeacherEditForm
from customuser.models import User
from customuser.forms import UserPasswordEditForm
from student.models import Student
from assignment.models import Assignment


def user_is_teacher_check(user):
    if user.is_authenticated:
        teacher = Teacher.objects.filter(user=user)
        if teacher.count() > 0:
            return True
    return False


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def classroom_create_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ClassroomCreateForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = Teacher.objects.get(user=request.user)
            classroom.save()
            return redirect(reverse('teacher:classroom_detail', kwargs={'slug': classroom.slug}))
        else:
            form = ClassroomCreateForm()
            return render(request, 'classroom_create.html', {'form': form})
    else:
        form = ClassroomCreateForm()
    return render(request, 'classroom_create.html', {'form': form})


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def home_page_view(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    queryset = TeachersClassRoom.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'classrooms': queryset
    }
    return render(request, 'teacher_window.html', context=context)


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def classroom_detail_view(request, slug):
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        raise Http404
    assignment_query = Assignment.objects.filter(classroom=classroom)
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query,
    }
    return render(request, 'classroom_detail.html',  context)


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def get_student_list(request, slug):
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        raise Http404
    students = classroom.student_set.all()
    context = {
        'classroom': classroom,
        'students': students
    }
    return render(request, 'get_student_list.html',  context)


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def teacher_edit_view(request):
    teacher = Teacher.objects.get(user=request.user)
    password_change_form = UserPasswordEditForm()
    teacher_edit_form = TeacherEditForm()
    if request.method == 'POST':
        if 'teacheredit_submit' in request.POST:
            teacher_edit_form = TeacherEditForm(request.POST)
            if teacher_edit_form.is_valid():
                teacher.name = teacher_edit_form.cleaned_data['name']
                teacher.department = teacher_edit_form.cleaned_data['department']
                teacher.save()
                new_phone = teacher_edit_form.cleaned_data['phone']
                if teacher.can_take_phone_number(new_phone):
                    teacher.update_phone_number(new_phone)
                    messages.success(request, 'Profile updated succesfully')
                else:
                    messages.error(request, 'Phone Number already exists.')
                    return render(request, 'teacher_editprofile.html', {
                        'passwordEditForm': password_change_form,
                        'teacherEditForm': teacher_edit_form,
                        'teacher': teacher
                    })
                return redirect('teacher:homepage')

        else:
            teacherEditForm = TeacherEditForm(instance=teacher)
            password_change_form = UserPasswordEditForm(request.POST)
            if password_change_form.is_valid():
                user = request.user
                old_password = password_change_form.cleaned_data['old_password']
                new_password = password_change_form.cleaned_data['new_password']
                confirm_password = password_change_form.cleaned_data['confirm_password']
                if user.check_password(old_password) and new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    user = authenticate(
                        request, username=user.email, password=new_password)
                    if user is not None:
                        login(request, user)
                        messages.success(
                            request, 'Password is updated successfully')
                        return redirect('teacher:homepage')
                elif new_password != confirm_password:
                    messages.error(
                        request, 'new password and confirm password must be same')
                else:
                    messages.error(request, 'Current Password is not correct.')
                return render(request, 'teacher_editprofile.html', {
                    'passwordEditForm': password_change_form,
                    'teacherEditForm': teacher_edit_form,
                    'teacher': teacher
                })
    else:
        teacher_edit_form = TeacherEditForm(instance=teacher)
        password_change_form = UserPasswordEditForm()
    return render(request, 'teacher_editprofile.html', {
        'teacherEditForm': teacher_edit_form,
        'passwordEditForm': password_change_form,
        'teacher': teacher
    })


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def classroom_delete_view(request, slug):
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        raise Http404
    classroom.delete()
    messages.success(request, "Successfully deleted")
    return redirect('teacher:homepage')


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def classroom_edit_view(request, slug):
    form = ClassroomCreateForm()
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ClassroomCreateForm(request.POST)
        if form.is_valid():
            classroom.title = form.cleaned_data['title']
            classroom.subject = form.cleaned_data['subject']
            classroom.section = form.cleaned_data['section']
            classroom.save()
            messages.success(
                request, "Classroom desctription has been updated")
            return redirect(reverse('teacher:classroom_detail', kwargs={'slug': slug}))
        else:
            messages.error(request, "Please enter valid details")
    else:
        form = ClassroomCreateForm(instance=classroom)
    return render(request, 'classroom_edit_view.html', {'form': form})

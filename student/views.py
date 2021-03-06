from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth import logout

from teacher.models import TeachersClassRoom
from assignment.models import Assignment
from .models import Student
from .forms import StudentRegistrationForm
from .forms import JoinClassForm
from .forms import SolutionCreateForm
from customuser.forms import UserPasswordEditForm

def user_is_student_check(user):
    if user.is_authenticated and user.is_student:
        return True
    else:
        return False


def user_is_student_registered(user):
    if user_is_student_check(user):
        if Student.is_student_registered(user):
            return True
        return False
    return False


@user_passes_test(user_is_student_check, login_url='customuser:permission_denied')
def HomePageViewStudent(request, *args, **kwargs):
    if request.user.is_active:
        if not Student.is_student_registered(request.user):
            return redirect(reverse('student:registration'))
        student = Student.get_student(user=request.user)
        classrooms = student.my_classes.all()
        return render(request, 'student_window.html',
                    {'classrooms': classrooms, 'student': student})
    else:
        messages.error(request, "The email address is not verified")
        return redirect('customuser:homepage')


@user_passes_test(user_is_student_check, login_url='customuser:permission_denied')
def StudentRegistration(request, *args, **kwargs):
    if not Student.is_student_registered(user=request.user):
        if(request.method == 'POST'):
            form = StudentRegistrationForm(request.POST)
            rollno = request.POST['rollno']
            student = Student.objects.filter(rollno=rollno)
            if student.count() == 0:
                if form.is_valid():
                    name = form.cleaned_data['name']
                    year = form.cleaned_data['year']
                    branch = form.cleaned_data['branch']
                    rollno = form.cleaned_data['rollno']
                    user = request.user
                    student_obj = Student(
                        name=name, year=year, branch=branch, rollno=rollno, user=user)
                    student_obj.save()
                    return redirect('student:homepage')
                else:
                    messages.error(request, "Incorrect Details")
            else:
                messages.error(request, "Roll number is already registered")
        else:
            form = StudentRegistrationForm()
        return render(request, 'register_student.html', {'form': form})
    else:
        return redirect('student:homepage')


@user_passes_test(user_is_student_registered, login_url='customuser:permission_denied')
def join_class_view(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            try:
                classroom = TeachersClassRoom.objects.get(class_id=class_id)
                student = Student.objects.get(user=request.user)
                student.my_classes.add(classroom)
                student.save()
            except ObjectDoesNotExist:
                messages.error(request, 'Please enter a valid class code')
                return render(request, 'join_class.html', {'form': form})
            messages.success(request,"Successfully joined.")
            return redirect('student:homepage')
    else:
        form = JoinClassForm()
    return render(request, 'join_class.html', {'form': form})


@user_passes_test(user_is_student_registered, login_url='customuser:permission_denied')
def classroom_detail_view(request, slug):
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
    except:
        messages.error(request, "Permission Denied")
        return redirect('customuser:permission_denied')
    assignment_query = Assignment.objects.filter(classroom=classroom).order_by('-pub_date')
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query,
    }
    return render(request, 'classroom_detail.html',  context)


@user_passes_test(user_is_student_registered, login_url='customuser:permission_denied')
def classroom_exit_view(request, slug):
    student = Student.objects.get(user=request.user)
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug)
    except:
        messages.error(request, 'You are not registered to classroom')
        return redirect('customuser:permission_denied')
    student.my_classes.remove(classroom)
    student.save()
    messages.success(request, "Successfully exit the classroom")
    return redirect('student:homepage')

@user_passes_test(user_is_student_registered, login_url='customuser:permission_denied')
def student_edit_view(request):
    student = Student.objects.get(user=request.user)
    password_change_form = UserPasswordEditForm()
    student_edit_form = StudentRegistrationForm
    if request.method == 'POST':
        if 'studentedit_submit' in request.POST:
            student_edit_form = StudentRegistrationForm(request.POST)
            if student.can_get_rollnumber(request.POST['rollno']):
                if student_edit_form.is_valid():
                    student.name = student_edit_form.cleaned_data['name']
                    student.year = student_edit_form.cleaned_data['year']
                    student.branch = student_edit_form.cleaned_data['branch']
                    student.rollno = student_edit_form.cleaned_data['rollno']
                    user = request.user
                    student.save()
                    messages.success(request, "Profile updated successfully")
                    return redirect('student:homepage')
            
                else:
                    messages.error(request, "Incorrect Details")
            else:
                messages.error(request, "Roll number is already registered")

        else:
            student_edit_form = StudentRegistrationForm(instance=student)
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
                        return redirect('student:homepage')
                elif new_password != confirm_password:
                    messages.error(
                        request, 'New Password and Confirm Password must be same')
                else:
                    messages.error(request, 'Current Password is not correct.')
                return render(request, 'student_edit_view.html', {
                    'passwordEditForm': password_change_form,
                    'studentEditForm': student_edit_form,
                    'student': student,
                })
    else:
        student_edit_form = StudentRegistrationForm(instance=student)
        password_change_form = UserPasswordEditForm()
    return render(request, 'student_edit_view.html', {
        'studentEditForm': student_edit_form,
        'passwordEditForm': password_change_form,
        'student': student
    })

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView

from customuser import urls
from student import urls
from teacher.models import Teacher
from teacher.forms import TeacherRegistrationForm
from .models import User
from .forms import LoginForm, UserRegisterForm


def homepageview(request):
    if request.user.is_authenticated is False:
        if request.method == 'POST':
            form = TeacherRegistrationForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                department = form.cleaned_data['department']
                user_list = User.objects.filter(email=email)
                if user_list.count() is 0:
                    user = User.objects.create_user(
                        email=email, password=password)
                    user.is_teacher = True
                    user.is_active = True
                    group = Group.objects.get(name='teacher')
                    user.groups.add(group)
                    user.save()
                    teacherobj = Teacher(
                        name=name, department=department, phone=phone, user=user)
                    teacherobj.save()
                    messages.success(
                        request, "Successfully created. Login to give assignments")
                    return redirect('customuser:homepage')

                else:
                    messages.error(
                        request, "This email address is already registered")
            else:
                messages.error(request, "Form is invalid")

        else:
            form = TeacherRegistrationForm()
        return render(request, 'home.html', {'form': form})
    else:
        if request.user.is_teacher is True:
            return redirect('teacher:homepage')
        else:
            return redirect('student:homepage')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                if request.user.is_teacher is False:
                    return redirect('student:registration')
                else:
                    return redirect('teacher:homepage')
            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        print("signed up")
        form = UserRegisterForm(request.POST)
        try:
            form_obj = User.objects.get(email = request.POST['email'])
        except:
            form_obj = None
        if form_obj is None:
            if form.is_valid():
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(email=email, password=password)
                group = Group.objects.get(name='student')
                user.groups.add(group)
                user.is_active = True
                user.save()
                messages.success(request, "Successfully registered. Click on login and fill details.")
                return redirect('customuser:homepage')
            else:
                messages.error(request, "Incorrect details.")
        else:
            messages.error(request, "This email address is already registered. Click on login button.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')


def delete_user(request):
    user_obj = User.objects.filter(email=request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:homepage')


def contactus(request):
    return render(request, "contactus.html")

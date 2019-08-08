from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.views.generic import TemplateView
from student import urls
from teacher.forms import TeacherRegistrationForm
from customuser import urls
from teacher.models import Teacher
from .models import User
from .forms import LoginForm,UserAdminChangeForm, UserAdminCreationForm,UserRegisterForm


def create_teacher(form_data):
    password = form_data['password']
    email = form_data['email']
    name = form_data['name']
    phone = form_data['phone']
    department = form_data['department']
    user = User.objects.create_user(
        email=email, password=password)
    user.teacher_status = True
    user.save()
    teacherobj = Teacher(
        name=name, department=department, phone=phone, teacher_user=user)
    teacherobj.save()


def homepageview(request):
    if request.user.is_authenticated is False:
        teacherform = TeacherRegistrationForm()
        userform = UserRegisterForm()
        if request.method == 'POST':
            if 'userform_submit' in request.POST:
                userform = UserRegisterForm(request.POST)
                if userform.is_valid():
                    email = userform.cleaned_data['email']
                    password = userform.cleaned_data['password']
                    user = User.objects.create_user(email=email, password=password)
                    user.save()
                    return redirect('customuser:homepage')
                return render(request,'home.html',{'userform':userform})
            else:
                teacherform = TeacherRegistrationForm(request.POST)
                if teacherform.is_valid():
                    create_teacher(teacherform.cleaned_data)
                    messages.success(request, "Successfully created. Login to give assignments")
                else:
                    messages.error(request, 'Incorrect Details')
                return redirect('customuser:homepage')
        return render(request, 'home.html', {'userform': userform, 'teacherform': teacherform })
    
    elif request.user.is_authenticated and request.user.is_teacher is True:
        return redirect('teacher:teachers_homepage')
    
    elif request.user.is_authenticated and not request.user.is_teacher :
        if request.user.details:
            return redirect('student:student_homepage')
        else :
            return redirect('student:student_registration')

def login_view(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                print("teacher status")
                print(request.user.is_teacher)
                if request.user.is_teacher is False:
                    if request.user.details is True:
                        return redirect('student:student_homepage')
                    else:
                        return redirect('student:student_registration')
                else:
                    return redirect('teacher:teachers_homepage')

            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(email=email, password=password)
            user.save()
            return redirect('customuser:homepage')
    else:
        form = UserRegisterForm()
    return render(request,'student_signup.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')

def contactus(request):
    return render(request, "contactus.html")



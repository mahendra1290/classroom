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

def homepageview(request):
    if request.user.is_authenticated is False:
        if request.method=='POST':
            form = TeacherRegistrationForm(request.POST)
            print(form)
            print(form.is_valid())
            if form.is_valid():
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                phone=form.cleaned_data['phone']
                department = form.cleaned_data['department']
                user_list = User.objects.filter(email = email)
                print("USERLIST IS ")
                print(user_list)
                if user_list.count() is 0:
                    user = User.objects.create_user(email=email, password=password)
                    user.is_teacher = True
                    user.save()
                    teacherobj = Teacher(name=name,department=department,phone=phone,teacher_user=user)
                    teacherobj.save()
                    messages.success(request, "Successfully created. Login to give assignments")
                    return redirect('customuser:homepage')

                else:
                    messages.error(request, "This email address is already registered")
            else:
                message.error(request, "Form is invalid")
            
        else:
            form = TeacherRegistrationForm()
        return render(request,'home.html',{'form':form})
    else:
        if request.user.is_teacher is True:
            return redirect('teacher:teachers_homepage')
        else:
            if request.user.details is True:
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
                if request.user.is_teacher is False:
                    return redirect('student:student_homepage')
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
    return render(request,'signup.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:homepage')

def contactus(request):
    return render(request, "contactus.html")



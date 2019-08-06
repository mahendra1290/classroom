from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import LoginForm,UserAdminChangeForm, UserAdminCreationForm,UserRegisterForm

from .models import User
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student import urls
from teacher.forms import TeacherRegistrationForm
from customuser import urls
from teacher.models import Teacher

def homepageview(request):
    if not request.user.is_authenticated :
        teacherform = TeacherRegistrationForm()
        userform = UserRegisterForm()
        if request.method == 'POST':
            if 'loginform_submit' in request.POST:
                userform = UserRegisterForm(request.POST)
                if userform.is_valid():
                    print("USERFORM IS VALID")
                    email = userform.cleaned_data['email']
                    password = userform.cleaned_data['password']
                    print("email id ")
                    print(email)
                    user = User.objects.create_user(email=email, password=password)
                    user.save()
                    return redirect('customuser:homepage')
                else:
                    userform = UserRegisterForm()
                return render(request,'homepage.html',{'form':userform})


            else:
                userform = UserRegisterForm()
                teacherform = TeacherRegistrationForm(request.POST)
                if teacherform.is_valid():
                    password = teacherform.cleaned_data['password']
                    email = teacherform.cleaned_data['email']
                    name = teacherform.cleaned_data['name']
                    phone=teacherform.cleaned_data['phone']
                    department = teacherform.cleaned_data['department']
                    user = User.objects.create_user(email=email, password=password)
                    user.is_teacher = True
                    user.save()
                    teacherobj = Teacher(name=name,department=department,phone=phone,teacher_user=user)
                    teacherobj.save()
                    messages.success(request, "Successfully created. Login to give assignments")
                else:
                    messages.error(request, 'Incorrect Details')
                return redirect('customuser:homepage')

        return render(request, 'home.html', {'userform': userform, 'teacherform': teacherform })
    
    elif request.user.is_authenticated and request.user.is_teacher is True:
        return redirect('teacher:teachers_homepage')
    
    elif request.user.is_authenticated and not request.user.is_teacher :
        if request.user.details:
            return redirect('student : student_homepage')
        else :
            return redirect('student :student_registration')

def login_view(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                print(request.user.is_teacher)
                if request.user.is_teacher is False:
                    return redirect('student:student_registration')
                else:
                    return redirect('teacher:teachers_homepage')

            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'form': form})


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
    return redirect('customuser:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')

def contactus(request):
    return render(request, "contactus.html")



from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import LoginForm, UserStudentRegisterForm,UserAdminChangeForm, UserAdminCreationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import student
from student import urls
import assignment

class HomePageView(TemplateView):
    template_name = 'home_user.html'

def login_user(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                print(request.user.is_active)
                print(user_obj.is_teacher)
                return redirect('student:student_homepage')

            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_user_student(request):
    if request.method=='POST':
        form = UserStudentRegisterForm(request.POST)
        if form.is_valid():
            password_ = form.cleaned_data['password']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            rollno = form.cleaned_data['rollno']
            year = form.cleaned_data['year']
            branch = form.cleaned_data['branch']
            user = User.objects.create_user_student(email=email, password=password_,name=name,year=year,branch=branch, rollno = rollno)
            user.save()
            return redirect('customuser:home_user')
    else:
        form = UserStudentRegisterForm()
    return render(request,'signup_student.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('customuser:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')
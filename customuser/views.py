from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import LoginForm,UserAdminChangeForm, UserAdminCreationForm

from .models import User
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import student
from student import urls
import assignment
import teacher

class HomePageView(TemplateView):
    template_name = 'home_user.html'

def login_view(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                print(request.user.is_active)
                if request.user.is_teacher is False:
                    return redirect('student:student_registration')
                else:
                    return redirect('teacher:teacher_homepage')

            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password_ = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(email=email, password=password)
            user.save()
            return redirect('customuser:home')
    else:
        form = UserRegisterForm()
    return render(request,'signup.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('user:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('user:home_user')
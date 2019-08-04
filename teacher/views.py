from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import student
from student import urls
import assignment


# Create your views here.
def HomePageViewTeacher(request):
    return render(request, 'home_teacher.html')


def logout_view(request):
    logout(request)
    return redirect('user:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('user:home_user')
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from user.models import User
from user import urls


def HomePageViewStudent(request , *args , **kwargs):
    print(request)
    print(request.user)
    return render(request,'home_student.html' )

def logout_view(request):
    logout(request)
    return redirect('user:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('user:home_user')
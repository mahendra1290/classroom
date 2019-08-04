from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from customuser.models import User
from customuser import urls
from .forms import StudentRegistrationForm
from .models import Student

def HomePageViewStudent(request , *args , **kwargs):
    print(request)
    print(request.user)
    return render(request,'home_student.html' )

def StudentRegistration(request, *args , **kwargs):
    if request.user.details is False:
        if(request.method=='POST'):
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                student_obj = Student()
                student_obj.name = form.cleaned_data['name']
                student_obj.year = form.cleaned_data['year']
                student_obj.branch = form.cleaned_data['branch']
                student_obj.rollno = form.cleaned_data['rollno']
                student_obj.student = request.user
                request.user.details = True
                student_obj.save()
                return redirect('student:student_homepage')
        else:
            form=StudentRegistrationForm()
        return render(request,'student_registration.html',{'form':form})
    else:
        return redirect('student:student_homepage')

def logout_view(request):
    logout(request)
    return redirect('customuser:home_user')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:home_user')
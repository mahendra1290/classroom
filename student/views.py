from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from customuser import urls
from .forms import StudentRegistrationForm
from .models import Student

def HomePageViewStudent(request , *args , **kwargs):
    return render(request,'student_window.html' )

def StudentRegistration(request, *args , **kwargs):
    if(request.method=='POST'):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            year = form.cleaned_data['year']
            branch = form.cleaned_data['branch']
            rollno = form.cleaned_data['rollno']
            student_user = request.user
            student_obj = Student(name=name,year=year,branch=branch,rollno=rollno,student_user=student_user)
            student_obj.save()
            request.user.details = True
            request.user.active = True
            request.user.save()
            return redirect('student:student_homepage')
    else:
        form=StudentRegistrationForm()
    return render(request,'register_student.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:homepage')
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from customuser import urls
from .forms import StudentRegistrationForm, JoinClassForm
from .models import Student
from teacher.models import TeachersClassRoom
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def HomePageViewStudent(request , *args , **kwargs):
    student = Student.objects.get(student_user=request.user)
    classroom_list = student.my_classes.all()
    print("clad---------fdjfoia*****************")
    print(classroom_list)
    print(student)
    print(student.my_classes.all())
    return render(request,'student_window.html',{'classroom_list':classroom_list})

def StudentRegistration(request, *args , **kwargs):
    if not request.user.details :    
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
    else:
        return redirect('student:student_homepage')


def join_class_view(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            try:
                classroom = TeachersClassRoom.objects.get(class_id=class_id)
                student = Student.objects.get(student_user=request.user)
                student.my_classes.add(classroom)
                student.save()
            except ObjectDoesNotExist:
                messages.error(request, 'Please enter a valid class code')
                return render(request, 'join_class.html', {'form':form})
            return redirect('student:student_homepage')
    else:
        form = JoinClassForm()
    return render(request, 'join_class.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')

def delete_user(request):
    user_obj = User.objects.filter(email = request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:homepage')

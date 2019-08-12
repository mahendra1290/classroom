from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from teacher.models import TeachersClassRoom
from assignment.models import Assignment
from .models import Student
from .forms import StudentRegistrationForm
from .forms import JoinClassForm


@login_required
def HomePageViewStudent(request , *args , **kwargs):
    if request.user.is_student:
        if not Student.is_student_registered(request.user):
            return redirect (reverse('student:registration'))
        student = Student.get_student(user=request.user)
        classrooms = student.my_classes.all()
        print(classrooms)
        assignment_list = []
        for i in classrooms:
            a = Assignment.objects.filter(classroom=i)
            if a.count() > 0:
                assignment_list.append(a[0])
        return render(request, 'student_window.html',
                      context={
                               'classrooms': classrooms,
                               'assignment_list': assignment_list
                               }
                      )
    else :
        raise PermissionDenied

@login_required
def StudentRegistration(request, *args , **kwargs):
    if not Student.is_student_registered(user=request.user):    
        if(request.method=='POST'):
            form = StudentRegistrationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                year = form.cleaned_data['year']
                branch = form.cleaned_data['branch']
                rollno = form.cleaned_data['rollno']
                user = request.user
                student_obj = Student(name=name,year=year,branch=branch,rollno=rollno,user=user)
                student_obj.save()
                return redirect('student:homepage')
        else:
            form=StudentRegistrationForm()
        return render(request,'register_student.html',{'form':form})
    else:
        return redirect('student:homepage')


def join_class_view(request):
    print(request.method)
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            try:
                classroom = TeachersClassRoom.objects.get(class_id=class_id)
                student = Student.objects.get(user=request.user)
                student.my_classes.add(classroom)
                student.save()
            except ObjectDoesNotExist:
                messages.error(request, 'Please enter a valid class code')
                return render(request, 'join_class.html', {'form':form})
            return redirect('student:homepage')
    else:
        form = JoinClassForm()
    return render(request, 'join_class.html', {'form':form})

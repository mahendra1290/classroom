from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, JoinClassForm
from .models import Student
from teacher.models import TeachersClassRoom
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from assignment.models import Assignment

def HomePageViewStudent(request , *args , **kwargs):
    if request.user.details is False:
        return redirect('student:student_registration')
    student = Student.objects.get(student_user=request.user)
    classroom_list = student.my_classes.all()
    assignment_list = []
    for i in classroom_list:
        a = Assignment.objects.filter(assignment_of_class=i)
        if a.count() > 0:
            assignment_list.append(a[0])
    print(classroom_list)
    return render(request,'student_window.html' , context={'classroom_list' : classroom_list, 'assignment_list':assignment_list})

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
                print("does not exist")
            return redirect('student:student_homepage')
    else:
        form = JoinClassForm()
    return render(request, 'join_class.html', {'form':form})

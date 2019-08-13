from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
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
from .forms import SolutionCreateForm


@login_required
def HomePageViewStudent(request, *args, **kwargs):
    if request.user.is_student:
        if not Student.is_student_registered(request.user):
            return redirect(reverse('student:registration'))
        student = Student.get_student(user=request.user)
        classrooms = student.my_classes.all()
        assignment_list = []
        for i in classrooms:
            a = Assignment.objects.filter(classroom=i)
            if a.count() > 0:
                assignment_list.append(a[0])
        return render(request, 'student_window.html',
                      context={
                               'classrooms': classrooms,
                               'assignment_list': assignment_list,
                               'student': student,
                      }
                      )
    else:
        raise PermissionDenied


@login_required
def StudentRegistration(request, *args, **kwargs):
    if not Student.is_student_registered(user=request.user):
        if(request.method == 'POST'):
            form = StudentRegistrationForm(request.POST)
            try:
                form_rollno = Student.objects.get(
                    rollno=request.POST['rollno'])
            except:
                form_rollno = None
            if form_rollno is None:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        year = form.cleaned_data['year']
                        branch = form.cleaned_data['branch']
                        rollno = form.cleaned_data['rollno']
                        user = request.user
                        student_obj = Student(
                            name=name, year=year, branch=branch, rollno=rollno, user=user)
                        student_obj.save()
                        return redirect('student:homepage')
                    else:
                        messages.error(request, "Incorrect Details")
            else:
                messages.error(request, "Roll number is already registered")
        else:
            form = StudentRegistrationForm()
        return render(request, 'register_student.html', {'form': form})
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
                return render(request, 'join_class.html', {'form': form})
            return redirect('student:homepage')
    else:
        form = JoinClassForm()
    return render(request, 'join_class.html', {'form': form})

def student_edit_view(request):
    student = Student.objects.get(user = request.user)
    print(student)
    if Student.is_student_registered(user=request.user):
        if(request.method == 'POST'):
            form = StudentRegistrationForm(request.POST)
            try:
                form_rollno = Student.objects.get(
                    rollno=request.POST['rollno'])
                if form_rollno == Student.objects.get(rollno = student.rollno):
                    form_rollno=None
            except:
                form_rollno = None
            if form_rollno is None:
                    if form.is_valid():
                        student.name = form.cleaned_data['name']
                        student.year = form.cleaned_data['year']
                        student.branch = form.cleaned_data['branch']
                        student.rollno = form.cleaned_data['rollno']
                        user = request.user
                        student.save()
                        messages.success(request, "Profile updated successfully")
                        return redirect('student:homepage')
                    else:
                        messages.error(request, "Incorrect Details")
            else:
                messages.error(request, "Roll number is already registered")
        else:
            form = StudentRegistrationForm(initial={'name':student.name, 'year':student.year, 'branch':student.branch,'rollno':student.rollno})
        return render(request, 'student_edit_view.html', {'form': form})
    else:
        return redirect('student:homepage')

def classroom_detail_view(request, pk):
    classroom = TeachersClassRoom.objects.get(id=pk)
    assignment_query = Assignment.objects.filter(classroom=classroom)
    context = {
        'classroom': classroom,
        'assignment_list': assignment_query,
    }
    return render(request, 'classroom_detail.html',  context)


def classroom_exit_view(request,pk):
    classroom = TeachersClassRoom.objects.get(pk=pk)
    if classroom is not None:
        student.my_classes.remove(classroom)
        student.save()
        messages.success(request, "Successfully exit the classroom")
    else: 
        messages.error(request, 'Classroom doesnot exist')
    return redrect('student:homepage')
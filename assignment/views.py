import os

from django.views.generic.edit import FormView
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from teacher.models import Teacher
from teacher.models import TeachersClassRoom
from student.models import Solution
from .forms import AssignmentCreateForm
from .models import AssignmentsFile
from .models import Assignment
from student.forms import SolutionCreateForm
from student.models import Student, Solution, SolutionFile


def user_is_teacher_check(user):
    if user.is_authenticated:
        teacher = Teacher.objects.filter(user=user)
        if teacher.count() > 0:
            return True
    return False


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def add_assignment_view(request, pk_of_class):
    try:
        classroom = TeachersClassRoom.objects.get(id=pk_of_class)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES)
        print(form)
        files = request.FILES.getlist('assign_file')
        print(form.is_valid())

        if form.is_valid():
            classroom = TeachersClassRoom.objects.get(id=pk_of_class)
            assign = Assignment(
                title=form.cleaned_data['title'],
                instructions=form.cleaned_data['instructions'],
                classroom=classroom,
                due_date=form.cleaned_data['due_date']
            )
            assign.save()
            for f in files:
                assignment_file = AssignmentsFile(file=f, assignment=assign)
                assignment_file.save()
            return HttpResponseRedirect(reverse_lazy('teacher:classroom_detail' , args=(pk_of_class,)))
    else:
        form = AssignmentCreateForm()

    return render(request, 'assignment.html', {'form': form,'classroom':classroom})

def assignment_view(request, pk, *args, **kwargs):
    assignment = Assignment.objects.get(id=pk)
    files = list(AssignmentsFile.objects.filter(assignment = assignment))
    if not request.user.is_student:
        classroom_id = assignment.classroom.id
        classroom = TeachersClassRoom.objects.get(pk = classroom_id)
        students = classroom.student_set.all()
        students_count = students.count()
        solutions = Solution.objects.filter(assignment=assignment)
        solutions_count = solutions.count()
        context = {
            'assignment' : assignment,
            'assignment_files' : files,
            'solutions' : solutions,
            'solutions_count':solutions_count,
            'students_count':students_count,
        }
        return render(request, "index.html", context)
    else:
        context= {
            'assignment':assignment,
            'assignment_files' : files,
        }
        return render(request, "student_assignment_view.html", context)


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def assignment_delete_view(request, pk,*args, **kwargs):
    assignment = Assignment.objects.get(id=pk)
    classroom_id = assignment.classroom.id 
    url = reverse_lazy('teacher:classroom_detail', kwargs={'pk': classroom_id})
    teacher_email = (assignment.classroom.teacher.user.email)
    if assignment is not None and request.user.email==teacher_email:
        assignment.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "Please enter a valid class Id")
        return redirect('teacher:homepage')
    return HttpResponseRedirect(url)

def assignment_file_view(request, pk, *args, **kwargs):
    assignment = Assignment.objects.get(id=pk)
    files = (AssignmentsFile.objects.filter(assignment = assignment))
    print(files)
    context = {
        'assignment_files' : files,
    }
    return render(request, "assignment_file_view.html", context)

def is_student_slug_used(student_slug):
    try:
        solution = Solution.objects.get(student_slug=student_slug)
        return True
    except ObjectDoesNotExist:
        return False

def solution_create_view(request, pk, *args, **kwargs):
    try:
        assignment =Assignment.objects.get(id = pk)
        student = Student.objects.get(user = request.user)
        sol  =Solution.objects.get(assignment=assignment, student=student)
    except:
        sol=None
    if sol is not None:    
        solfiles = SolutionFile.objects.filter(submission=sol)
    else:
        solfiles=None
    if solfiles is None:
        count=0
        form  = SolutionCreateForm()
        if request.method=='POST':
            form  = SolutionCreateForm(request.POST,request.FILES)
            files = request.FILES.getlist('solution_file')
            print(form)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                while True:
                    student_slug = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuv0123456789')
                    if not is_student_slug_used(student_slug):
                        break
                solution_obj = Solution(comment=comment,student = student, assignment=assignment,student_slug=student_slug)
                solution_obj.save()
                for f in files:
                    solution_file = SolutionFile(file=f, submission=solution_obj)
                    solution_file.save()
                messages.success(request, "Solution to assignment is successfully submitted")
                return redirect('customuser:homepage')
            else:
                messages.error(request, "Please enter valid info")
        return render(request,'student_solution_view.html',{'form':form, 'assignment':assignment,'count':count})
    else:
        count =1
        return render(request,'student_solution_view.html',{'solution_files':solfiles,'count':count,'assignment':assignment})


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def see_student_solution(request, pk,student_slug, *args, **kwargs):
    sol  =Solution.objects.get(student_slug=student_slug)
    assignment = Assignment.objects.get(pk =pk)
    solfiles = SolutionFile.objects.filter(submission=sol)
    student = sol.student
    return render(request,'see_student_solution.html',{'solution_files':solfiles,'assignment':assignment, 'student':student})



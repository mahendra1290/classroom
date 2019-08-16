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
from student.forms import SolutionCreateForm
from student.models import Solution
from student.models import Student, Solution, SolutionFile
from .forms import AssignmentCreateForm
from .models import AssignmentsFile
from .models import Assignment


def user_is_teacher_check(user):
    if user.is_authenticated:
        teacher = Teacher.objects.filter(user=user)
        if teacher.count() > 0:
            return True
    return False


@user_passes_test(user_is_teacher_check, login_url='customuser:permission_denied')
def add_assignment_view(request, slug_of_class):
    try:
        classroom = TeachersClassRoom.objects.get(slug=slug_of_class)
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        return render(request, '404.html')
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES)
        files = request.FILES.getlist('assign_file')
        if form.is_valid():
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
            return HttpResponseRedirect(reverse_lazy('teacher:classroom_detail' , args=(slug_of_class,)))
    else:
        form = AssignmentCreateForm()
    return render(request, 'assignment.html', {'form': form,'classroom':classroom})

def assignment_view(request, slug, *args, **kwargs):
    assignment = Assignment.objects.get(slug=slug)
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
def assignment_delete_view(request, slug,*args, **kwargs):
    try :
        assignment = Assignment.objects.get(slug=slug)
        classroom = assignment.classroom
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        return render(request, '404.html')
    assignment.delete()
    messages.success(request, "Successfully deleted")
    return HttpResponseRedirect(reverse_lazy('teacher:classroom_detail', kwargs={'slug': classroom.slug}))

def assignment_file_view(request, slug, *args, **kwargs):
    try:
        assignment = Assignment.objects.get(slug=slug)
        classroom = assignment.classroom
        if not classroom.belongs_to_teacher(request.user):
            return render(request, '404.html')
    except ObjectDoesNotExist:
        return render(request, '404.html')
    files = assignment.get_files()
    context = {
        'assignment_files' : files,
    }
    return render(request, "assignment_file_view.html", context)


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
            if form.is_valid():
                comment = form.cleaned_data['comment']
                solution_obj = Solution(comment=comment,student = student, assignment=assignment)
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
def see_student_solution(request, slug_of_assignment, slug, *args, **kwargs):
    sol  =Solution.objects.get(slug=slug)
    assignment = Assignment.objects.get(slug = slug_of_assignment)
    solfiles = SolutionFile.objects.filter(submission=sol)
    student = sol.student
    return render(request,'see_student_solution.html',{'solution_files':solfiles,'assignment':assignment, 'student':student})



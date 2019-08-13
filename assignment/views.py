from django.views.generic.edit import FormView
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from teacher.models import TeachersClassRoom
from student.models import Solution
from .forms import AssignmentCreateForm
from .models import AssignmentsFile
from .models import Assignment
from django.contrib import messages
from django.core.files import File
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from student.forms import SolutionCreateForm
from student.models import Student, Solution, SolutionFile


def add_assignment_view(request, pk_of_class):
    classroom = TeachersClassRoom.objects.get(id=pk_of_class)
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

def assignment_delete_view(request, pk,*args, **kwargs):
    assignment = Assignment.objects.get(id=pk)
    classroom_id = assignment.classroom.id 
    url = reverse('teacher:classroom_detail', kwargs={'pk': classroom_id})
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


def solution_create_view(request, pk, *args, **kwargs):
    assignment =Assignment.objects.get(id = pk)
    form  = SolutionCreateForm()
    if request.method=='POST':
        form  = SolutionCreateForm(request.POST,request.FILES)
        files = request.FILES.getlist('solution_file')
        print(form)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            student = Student.objects.get(user = request.user)
            solution_obj = Solution(comment=comment,student = student, assignment=assignment)
            solution_obj.save()
            for f in files:
                solution_file = SolutionFile(file=f, submission=solution_obj)
                solution_file.save()
            messages.success(request, "Solution to assignment is successfully submitted")
            return redirect('customuser:homepage')
        else:
            messages.error(request, "Please enter valid info")
    return render(request,'student_solution_view.html',{'form':form, 'assignment':assignment})



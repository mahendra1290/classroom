from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView
from .forms import AssignmentCreateForm
from .models import AssignmentsFile, Assignment
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from teacher.models import TeachersClassRoom
from django.http import HttpResponseRedirect

class AssignmentDeleteView(DeleteView):
    model = Assignment
    def get(self, request, pk_of_class, pk):
        return HttpResponse(render(request, 'assignment/assignment_confirm_delete.html'))
    success_url = reverse_lazy('')
    

def add_assignment_view(request, pk_of_class):
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
                assignment_of_class=classroom,
                due_date=form.cleaned_data['due_date']
            )
            assign.save()
            for f in files:
                assignment_file = AssignmentsFile(file=f, assignment=assign)
                assignment_file.save()
            return HttpResponseRedirect(reverse_lazy('teacher:classroom_detail' , args=(pk_of_class,)))
    else:
        form = AssignmentCreateForm()

    return render(request, 'assignment.html', {'form': form})

def assignment_view(request, pk, *args, **kwargs):
    a = Assignment.objects.get(id=pk)
    files = list(AssignmentsFile.objects.filter(assignment = a))
    context = {
        'assignment' : a,
        'assignment_files' : files
    }
    return render(request, "index.html", context)


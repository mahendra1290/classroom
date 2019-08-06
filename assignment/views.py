from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView
from .forms import AssignmentCreateForm
from .models import AssignmentsFile, Assignment
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy

class AssignmentDeleteView(DeleteView):
    model = Assignment
    class_id = 0
    def get(self, request, pk_of_class, pk):
        success_url = reverse_lazy('teacher:classroom_detail', args=(pk_of_class,))
        return HttpResponse(render(request, 'assignment/assignment_confirm_delete.html'))
    

class AssignmentCreateView(FormView):
    prime_key = 0
    form_class = AssignmentCreateForm
    template_name = 'assignment.html'  # Replace with your template.
    success_url = f'{prime_key}/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('assign_file')
        if form.is_valid():
            data = form.cleaned_data['title']
            #inst = form.cleaned_data['instructions']
            print(form.cleaned_data)
            print(files)
            assign = Assignment(title = form.cleaned_data['title'], instructions = form.cleaned_data['instruction'])
            assign.save()
            for f in files:
                assignment_file = AssignmentsFile(file = f, assignment = assign)
                assignment_file.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def assignment_view(request, pk, *args, **kwargs):
    a = Assignment.objects.get(id=pk)
    files = list(AssignmentsFile.objects.filter(assignment = a))
    context = {
        'assignment' : a,
        'assignment_files' : files
    }
    return render(request, "index.html", context)


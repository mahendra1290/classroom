from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView
from .forms import AssignmentCreateForm
from .models import AssignmentsFile, Assignment
from django.shortcuts import render

class AssignmentDeleteView(DeleteView):
    pass

class AssignmentCreateView(FormView):
    prime_key = 0
    form_class = AssignmentCreateForm
    template_name = 'index.html'  # Replace with your template.
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
    files = AssignmentsFile.objects.filter(assignment = a)[0]
    context = {
        'b' : a,
        'f' : files
    }

    return render(request, "assignment.html", context)


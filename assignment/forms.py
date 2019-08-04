from django import forms
from .models import Assignment, AssignmentsFile

class AssignmentCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    instruction = forms.CharField(max_length=100)
    pub_date = forms.DateField(required=False)
    due_date = forms.DateField(required=False)
    assign_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# class AssignmentFileUploadForm(forms.ModelForm):
#     class Meta:
#         model = AssignmentsFile
#         fields = ['file']
#         widgets = {
#             'file' : forms.ClearableFileInput(attrs = {'multiple' : True}),
#         }



from django import forms
from .models import Assignment, AssignmentsFile

class AssignmentCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    instruction = forms.CharField(max_length=100)
    pub_date = forms.DateField(required=False, widget = forms.DateInput(attrs={'class':'datepicker'}))
    due_date = forms.DateField(required=False, widget = forms.DateInput(attrs={'class':'datepicker'}))
    assign_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# class AssignmentFileUploadForm(forms.ModelForm):
#     class Meta:
#         model = AssignmentsFile
#         fields = ['file']
#         widgets = {
#             'file' : forms.ClearableFileInput(attrs = {'multiple' : True}),
#         }



from django import forms
from .models import Assignment, AssignmentsFile
from datetime import date


class AssignmentCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    instruction = forms.CharField(max_length=100)
    due_date = forms.DateField(required=False, widget = forms.DateInput(attrs={'class':'datepicker'}))
    assign_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    # title =title=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}))
    # instruction = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Title'}))
    # # due_date = forms.DateField(widget = forms.DateInput(attrs = {'placeholder':'Date'}))

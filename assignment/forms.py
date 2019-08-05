from django import forms
from .models import Assignment, AssignmentsFile
from datetime import date


class AssignmentCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    instruction = forms.CharField(max_length=100)
    due_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    assign_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

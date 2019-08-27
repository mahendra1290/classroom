from django import forms
from .models import Assignment, AssignmentsFile
from datetime import date


class AssignmentCreateForm(forms.Form):
    class Meta:
        model = Assignment
        fields = ['title', 'instructions', 'due_date', 'assign_file', ]

    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Title','class': 'border w-100 p-2 bg-white text-capitalize'}))
    instructions = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Give any instructions','class':'border p-3 w-100'}))
    assign_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True,'class': '' ,'onchange' :'myFunction()'}))
    due_date = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=forms.DateTimeInput(attrs={
            'class': ' datetimepicker-input bg-white form-control',
            'data-target': '#datetimepicker1',

            'placeholder': 'Enter Submission Date',
        })
    )

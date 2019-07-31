from django import forms
from .models import Assignment, AssignmentsImage

class AssignmentCreateForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = all

class ImageForm(forms.ModelForm):

    class Meta:
        model = AssignmentsImage
        fields = all

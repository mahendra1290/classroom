
from django import forms
from .models import Teacher

class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['name',]

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    
from django.forms import ModelForm 
from .models import TeachersClassRoom


class ClassroomCreateForm(ModelForm):
    class Meta:
        model =  TeachersClassRoom
        fields = ['title', 'section', 'subject']


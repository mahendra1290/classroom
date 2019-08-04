from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','rollno','year','branch']

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))



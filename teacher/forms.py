
from django import forms
from .models import Teacher
from .models import TeachersClassRoom

class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['name','department','phone',]

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name','class': 'border p-3 w-100 my-2'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email','class': 'border p-3 w-100 my-2'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','class': 'border p-3 w-100 my-2'}))
    phone = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder':'Phone','class': 'border p-3 w-100 my-2'}))
    



class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model =  TeachersClassRoom
        fields = ['title', 'section', 'subject']
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title','class': 'border p-3 w-100 my-2'}))
    section = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Section','class': 'border p-3 w-100 my-2'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Subject','class': 'border p-3 w-100 my-2'}))

class TeacherEditForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['name','department','phone',]

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name','class': 'border p-3 w-100 my-2'}))
    phone = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder':'Phone','class': 'border p-3 w-100 my-2'}))
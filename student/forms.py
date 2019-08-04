from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','rollno','year','branch','category']

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    rollno = forms.NumberInput(widget = forms.NumberInput(attrs={'placeholder':'RollNUmber'}))









        #         title =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','class': 'border w-100 p-2 bg-white text-capitalize'}))
        # description=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Describe Your Product','class':'border p-3 w-100'}))
        # price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Price','class': 'border-0 py-2 w-100 price'}))
        # # image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file d-none'}))
        # image = forms.ImageField()
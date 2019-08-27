from django import forms
from .models import Student
from .models import Solution

YEAR_CHOICES = (
    ('', 'Select Year'),
    ('firstyear','First Year'),
    ('secondyear','Second Year'),
    ('thirdyear','Third Year'),
    ('fourthyear','Fourth Year'),
)
BRANCH_CHOICES = (
    ('', 'Select Branch'),
    ('cse', 'Computer Engg.'),
    ('ee', 'Electrical Engg.'),
    ('ece', 'Electronics and Comm. Engg.'),
    ('me', 'Mechanical Engg.'),
    ('pie', 'Production and Industial Engg.'),
    ('ce', 'Civil Engg.'),

)
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','rollno','year','branch']

    name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name','class': 'border p-3 w-100 my-2', 'required':'required'}))
    rollno = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'RollNo','class': 'border p-3 w-100 my-2','required':'required'}))
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'required':'required'}))
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, widget=forms.Select(attrs={'required':'required'}))

class JoinClassForm(forms.Form):
    class_id = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'class code','class': 'border p-3 w-100 my-2', 'required':'required'}))
    class Meta:
        fields=['class_id']



class SolutionCreateForm(forms.Form):
    class Meta:
        model = Solution
        fields = ['comment', 'solution_file', ]

    comment = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'write comments if any','class':'border p-3 w-100'}))
    solution_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True,'class': '','onchange' :'myFunction()'}))

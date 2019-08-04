from django.forms import ModelForm 
from .models import TeachersClassRoom


class ClassroomCreateForm(ModelForm):
    class Meta:
        model =  TeachersClassRoom
        fields = ['title', 'section', 'subject']

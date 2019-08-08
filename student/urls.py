
from django.urls import path
from django.contrib.auth import authenticate, login,logout
from .views import join_class_view, StudentRegistration, HomePageViewStudent
from django.conf.urls import url


app_name="student"

urlpatterns = [
    path('join-class/', join_class_view, name='join_class' ),
    path('registration/', StudentRegistration, name = 'student_registration'),
    path('window/',HomePageViewStudent, name= 'student_homepage'),
]
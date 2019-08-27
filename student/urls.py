
from django.urls import path
from django.contrib.auth import authenticate, login,logout
from .views import join_class_view, StudentRegistration, HomePageViewStudent,student_edit_view,classroom_detail_view,classroom_exit_view
from django.conf.urls import url
from django.urls import include


app_name="student"

urlpatterns = [
    path('',HomePageViewStudent, name= 'homepage'),
    path('join-class/', join_class_view, name='join_class' ),
    path('edit/', student_edit_view, name='student_edit_view' ),
    path('registration/', StudentRegistration, name = 'registration'),
    path('classroom/<str:slug>/', classroom_detail_view, name='classroom_detail'),
    path('classroom/<str:slug>/exit', classroom_exit_view, name='classroom_exit_view'),
    path('classroom/<str:slug_of_class>/assignment/', include('assignment.urls')),
]
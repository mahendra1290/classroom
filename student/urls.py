
from django.urls import path
from django.contrib.auth import authenticate, login,logout
from . import views
from django.conf.urls import url


app_name="student"

urlpatterns = [
    path('window/',views.HomePageViewStudent, name= 'student_homepage'),
    path('delete/',views.delete_user, name = 'delete_user'),
    path('logout/', views.logout_view, name = 'logout'),
  

]
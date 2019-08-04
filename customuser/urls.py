
from django.urls import path
from django.contrib.auth import authenticate, login,logout
from . import views
from django.conf.urls import url


app_name="customuser"

urlpatterns = [
    path('', views.HomePageView.as_view(), name= 'home_user'),
    path('delete/',views.delete_user, name = 'delete_user'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
  

]
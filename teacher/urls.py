
from django.urls import path
from django.urls import include
from django.contrib.auth import authenticate, login,logout
from django.conf.urls import url
from .views import HomePageListView
from .views import ClassroomCreateView
from .views import classroom_detail_view

app_name="teacher"

urlpatterns = [
    path('', HomePageListView.as_view(), name='teachers_homepage'),
    path('classroom/add/', ClassroomCreateView.as_view(), name='create_classroom'),
    path('classroom-<int:pk>/', classroom_detail_view, name='classroom_detail'),
    path('classroom-<int:pk_of_class>/assignment/', include('assignment.urls')),
]
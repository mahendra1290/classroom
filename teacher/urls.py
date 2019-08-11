
from django.urls import path
from django.urls import include
from django.contrib.auth import authenticate, login,logout
from django.conf.urls import url
from .views import home_page_view
from .views import ClassroomCreateView
from .views import classroom_detail_view
from .views import teacher_edit_view
from .views import classroom_delete_view
from .views import classroom_edit_view

app_name="teacher"

urlpatterns = [
    path('', home_page_view, name='teachers_homepage'),
    path('edit/profile/',teacher_edit_view,name = 'teachers_edit' ),
    path('classroom/add/', ClassroomCreateView.as_view(), name='create_classroom'),
    path('classroom-<int:pk>/', classroom_detail_view, name='classroom_detail'),
    path('classroom-<int:pk>/delete/', classroom_delete_view, name='classroom_delete'),
    path('classroom-<int:pk>/edit/', classroom_edit_view, name='classroom_edit'),
    path('classroom-<int:pk_of_class>/assignment/', include('assignment.urls')),
]
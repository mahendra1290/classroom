
from django.urls import path
from django.urls import include
from django.contrib.auth import authenticate, login,logout
from django.conf.urls import url
from .views import home_page_view
from .views import classroom_create_view
from .views import classroom_detail_view
from .views import teacher_edit_view
from .views import classroom_delete_view
from .views import classroom_edit_view
from .views import get_student_list

app_name="teacher"

urlpatterns = [
    path('', home_page_view, name='homepage'),
    path('edit/profile/',teacher_edit_view,name = 'teachers_edit' ),
    path('classroom/add/', classroom_create_view, name='create_classroom'),
    path('classroom/<str:slug>/', classroom_detail_view, name='classroom_detail'),
    path('classroom/<str:slug>/delete/', classroom_delete_view, name='classroom_delete'),
    path('classroom/<str:slug>/edit/', classroom_edit_view, name='classroom_edit'),
    path('classroom/<str:slug>/studentlist/', get_student_list, name='get_student_list'),
    path('classroom/<str:slug_of_class>/assignment/', include('assignment.urls')),
]
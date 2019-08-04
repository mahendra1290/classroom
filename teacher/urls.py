
from django.urls import path
from django.urls import include
from django.contrib.auth import authenticate, login,logout
from django.conf.urls import url
from .views import HomePageViewTeacher
from .views import delete_user
from .views import logout_view
from .views import ClassroomCreateView
from .views import ClassroomDetailView
from .views import ClassroomListView


app_name="teacher"

urlpatterns = [
    path('window/', HomePageViewTeacher, name= 'teacher_homepage'),
    path('delete/',delete_user, name = 'delete_user'),
    path('logout/', logout_view, name = 'logout'),
    path('my_classrooms/', ClassroomListView.as_view(), name='classroom_list'),
    path('classroom/add/', ClassroomCreateView.as_view(), name='create_classroom'),
    path('classroom/<int:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
    path('assignment/', include("assignment.urls"))

]

from django.urls import path
from django.urls import include
from django.contrib.auth import authenticate, login,logout
from django.conf.urls import url
from .views import HomePageListView
from .views import delete_user
from .views import logout_view
from .views import ClassroomCreateView
from .views import ClassroomDetailView
from .views import classroom_detail_view
app_name="teacher"

urlpatterns = [
    path('', HomePageListView.as_view(), name='teachers_homepage'),
    path('delete/',delete_user, name = 'delete_teacher'),
    path('logout/', logout_view, name = 'logout'),
    path('classroom/add/', ClassroomCreateView.as_view(), name='create_classroom'),
    path('classroom/<int:pk>/', classroom_detail_view, name='classroom_detail'),
    path('assignment/', include("assignment.urls"))
]
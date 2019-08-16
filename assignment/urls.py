from django.urls import path
from .views import add_assignment_view
from .views import assignment_view
from .views import assignment_delete_view
from .views import assignment_file_view,solution_create_view,see_student_solution
from django.conf import settings
from django.conf.urls.static import static

app_name= "assignment"

urlpatterns = [
    path('<str:slug>', assignment_view, name = 'detail'),   
    path('<str:slug>/files', assignment_file_view, name = 'assignment_file_view'),  
    path('<str:slug>/solution-submit', solution_create_view, name = 'solution_create_view'),  
    path('add/', add_assignment_view, name = 'create'),
    path('delete/<str:slug>', assignment_delete_view, name = 'delete'),
    path('<str:slug_of_assignment>/solution/<str:slug>', see_student_solution, name = 'see_student_solution'),  
]

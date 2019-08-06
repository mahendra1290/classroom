from django.urls import path
from .views import add_assignment_view
from .views import assignment_view
from .views import AssignmentDeleteView



app_name= "assignment"



urlpatterns = [
    path('<int:pk>', assignment_view, name = 'assignment_detail'),   
    path('add/', add_assignment_view, name = 'create_assignment'),
    path('delete/<int:pk>', AssignmentDeleteView.as_view(), name = 'delete_assignment'),
]
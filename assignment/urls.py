from django.urls import path
from .views import add_assignment_view
from .views import assignment_view
from .views import assignment_delete_view

app_name= "assignment"

urlpatterns = [
    path('<int:pk>', assignment_view, name = 'detail'),   
    path('add/', add_assignment_view, name = 'create'),
    path('delete/<int:pk>', assignment_delete_view, name = 'delete'),
]
from django.urls import path
from .views import add_assignment_view
from .views import assignment_view
from .views import assignment_delete_view
from .views import assignment_file_view
from django.conf import settings
from django.conf.urls.static import static

app_name= "assignment"

urlpatterns = [
    path('<int:pk>', assignment_view, name = 'detail'),   
    path('<int:pk>/files', assignment_file_view, name = 'assignment_file_view'),   
    path('add/', add_assignment_view, name = 'create'),
    path('delete/<int:pk>', assignment_delete_view, name = 'delete'),
]

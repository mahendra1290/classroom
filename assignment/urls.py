from django.urls import path
from .views import FileFieldView, assignment_view

urlpatterns = [
    path('', FileFieldView.as_view(), name = 'upload'),
    path('<int:pk>', assignment_view, name = 'assignment')
    
]

from django.urls import path
from django.conf.urls import url
from django.contrib.auth import authenticate, login,logout

from .views import homepageview
from .views import contactus
from .views import login_view
from .views import signup_view
from .views import logout_view
from .views import delete_user

app_name="customuser"

urlpatterns = [
    path('', homepageview, name= 'homepage'),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('signup/', signup_view, name = 'signup'),
    path('contact/', contactus, name = 'contact'),
]
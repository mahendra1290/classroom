
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import authenticate, login,logout

from .views import homepageview
from .views import contact_us
from .views import login_view
from .views import signup_view
from .views import logout_view
from .views import delete_user
from .views import permission_denied_view
from .views import activate,forgetpassword,changepassword

app_name="customuser"

urlpatterns = [
    path('', homepageview, name= 'homepage'),
    path('404/', permission_denied_view, name = 'permission_denied'),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('signup/', signup_view, name = 'signup'),
    path('contact/', contact_us, name = 'contact'),
    path('delete/', delete_user, name = 'delete'),
    path('forgetpassword/', forgetpassword, name = 'forgetpassword'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^changepassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        changepassword, name='changepassword'),

]
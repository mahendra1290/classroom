from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


from teacher.models import Teacher
from teacher.forms import TeacherRegistrationForm
from .models import User
from .forms import LoginForm
from .forms import UserRegisterForm
from .forms import ContactForm



def homepageview(request):
    if request.user.is_authenticated is False:
        if request.method == 'POST':
            form = TeacherRegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user_list = User.objects.filter(email=email)
                if user_list.count() is 0:
                    teacherobj = form.save(commit=False)
                    user = User.objects.create_user_for_teacher(
                        email=email, password=password)
                    teacherobj.user = user
                    teacherobj.save()
                    messages.success(
                        request, "Successfully created. Login to give assignments")
                    return redirect('customuser:login')

                else:
                    messages.error(
                        request, "This email address is already registered")
            else:
                messages.error(request, "Form is invalid")
        else:
            form = TeacherRegistrationForm()
        return render(request, 'home.html', {'form': form})
    else:
        if request.user.is_teacher:
            return redirect('teacher:homepage')
        else:
            return redirect('student:homepage')


def permission_denied_view(request):
    return render(request, '404.html')

  
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                if request.user.is_teacher:
                    return redirect('teacher:homepage')
                else:
                    return redirect('student:registration')
            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user_for_student(
                email=email, password=password)
            messages.success(
                request, "Successfully registered. Click on login and fill details.")
            return redirect('customuser:login')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user.count() > 0:
                messages.error(
                    request, "This email address is already registered")
            else:
                messages.error(request, "Incorrect details.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('customuser:homepage')


def delete_user(request):
    user_obj = User.objects.filter(email=request.user.email)[0]
    user_obj.delete()
    return redirect('customuser:homepage')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(form)
        if form.is_valid():
            current_site = get_current_site(request)
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0}/{1} has sent you a new message:\n\n{2}".format(
                        sender_name,sender_email, form.cleaned_data['message'])
            mail_subject = 'Contact Us Reply'
            email = EmailMessage(
                        mail_subject, message, to=['piyushbhutaniynr@gmail.com']
            )
            email.send()
            mail_subject = "Thanks for Contacting"
            message = "Thanks for contacting us.Please take a moment to share feedback on your conversation experience with us."
            email = EmailMessage(
                        mail_subject, message, to=[sender_email]
            )
            email.send()
            messages.success(request, "Thankyou for your response.")
            return redirect('customuser:homepage')
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


from teacher.models import Teacher
from teacher.forms import TeacherRegistrationForm
from .models import User
from .forms import LoginForm
from .forms import UserRegisterForm
from .forms import ContactForm
from .forms import ForgetPasswordForm,PasswordRecoveryForm


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
                    mail_subject = 'Activate your Maroon account.'
                    current_site = get_current_site(request)
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                        mail_subject, message, to=[email]
                    )
                    email.send()
                    messages.info(request,'Please confirm your email address to complete the registration')
                    return redirect('customuser:homepage')
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
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user_obj = User.objects.filter(email=username)
                if user_obj.count()>0:
                    user_obj=user_obj.first()
                    if user_obj.is_active:
                        user_obj = authenticate(username=username, password=password)
                        if user_obj is not None:
                            login(request, user_obj)
                            if request.user.is_teacher:
                                return redirect('teacher:homepage')
                            else:
                                return redirect('student:registration')
                        else:
                            messages.error(request, "Incorrect Username or Password")
                    else:
                        messages.error(request,"The entered email address is not verified")
                else:
                    messages.error(request, 'Incorrect Username or Password')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('customuser:homepage')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user_for_student(
                    email=email, password=password)
                mail_subject = 'Activate your Maroon account.'
                current_site = get_current_site(request)
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                email = EmailMessage(
                            mail_subject, message, to=[email]
                )
                email.send()
                messages.info(request,'Please confirm your email address to complete the registration')
                return redirect('customuser:homepage')
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
    else:
        return redirect('customuser:homepage')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,'confirm.html')
    else:
        return HttpResponse('Activation link is invalid!')

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
        if form.is_valid():
            current_site = get_current_site(request)
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0}/{1} has sent you a new message:\n\n{2}".format(
                        sender_name,sender_email, form.cleaned_data['message'])
            mail_subject = 'Contact Us Reply'
            email = EmailMessage(
                        mail_subject, message, to=['response.maroon@gmail.com']
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


def forgetpassword(request):
    if not request.user.is_authenticated:
        form =ForgetPasswordForm()
        if request.method=='POST':
            form = ForgetPasswordForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                user = User.objects.filter(email=email)
                if user.count()>0:
                    user=user.first()
                    mail_subject = 'Password Recovery'
                    current_site = get_current_site(request)
                    message = render_to_string('forget_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                                mail_subject, message, to=[email]
                    )
                    email.send()
                    messages.info(
                        request, 'Password recovery link has been sent to the registered email id')
                    return redirect('customuser:homepage')
            else:
                messages.error(request,"Invalid email address")
        
        return render(request,'forget.html',{'form':form})
    else:
        return redirect('customuser:homepage')

def changepassword(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = PasswordRecoveryForm()
        if request.method=='POST':
            form = PasswordRecoveryForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']
                if new_password==confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,'Password updated successfully')
                    return redirect('customuser:login')
                else:
                    messages.error(request,"Password doesnot match.")
            else:
                messages.error(request, "Invalid Details")
        return render(request,'changepassword.html',{'form':form})
    else:
        return HttpResponse('Activation link is invalid!')
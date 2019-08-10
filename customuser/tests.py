from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import login 
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from .models import User
from teacher.models import Teacher
from teacher.tests import create_teacher
from student.tests import create_student


class UserModelTest(TestCase):

    def setUp(self):
        self.email = "test_base_user@gmail.com"
        self.password = "testuser"
        self.base_user = User.objects.create_user(
            email=self.email, password=self.password)
        self.base_user.is_active = True
        self.base_user.save()
        
    def test_username_is_email(self):
        self.assertEqual(f'{self.base_user.get_username()}', self.email)
    
    def test_user_homepage_view_when_no_user_is_logged_in(self):
        response = self.client.get(reverse('customuser:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'home.html')
    
    def test_user_login_page(self):
        has_logined = self.client.login(username=self.base_user.get_username(), password='testuser')
        self.assertEqual(has_logined, True)
        response = self.client.get(reverse('customuser:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_logout_page(self):
        self.client.logout()
        response = self.client.get(reverse('customuser:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customuser:homepage'))

    def test_user_signup_view(self):
        response = self.client.post(reverse('customuser:signup'), 
            data={'email':'testsignup@gmail.com', 'password':'password'}
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customuser:homepage'))
    
    def test_user_is_registered(self):
        response = self.client.post(reverse('customuser:signup'),
            data={'email': 'testsignup@gmail.com', 'password': 'password'}
        )
        user = User.objects.filter(email='testsignup@gmail.com')
        self.assertEqual(user.count(), 1)

    def test_teacher_user_redirected_to_correct_homepage(self):
        teacher = create_teacher(
            name="teacher",
            email="teacher@gmail.com",
            password="teacher",
            department="cs",
            phone=1234567891
        )
        response = self.client.post(reverse('customuser:login'), data={
            'email' : 'teacher@gmail.com',
            'password':'teacher'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher:homepage'))
    
    def test_student_user_redirected_to_correct_homepage(self):
        student = create_student(
            email='student@gmail.com',
            password='student'
        )
        response = self.client.post(reverse('customuser:login'), data={
            'email' : 'student@gmail.com',
            'password' : 'student'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student:homepage'))


    

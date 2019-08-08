from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth import login , authenticate, logout
from .models import User
from teacher.models import Teacher


class UserModelTest(TestCase):

    def setUp(self):
        self.email = "test_base_user@gmail.com"
        self.password = "testuser"
        self.base_user = User.objects.create_user(
            email=self.email, password=self.password)
        self.base_user.save()
        self.super_user = User.objects.create_superuser(
            email="super@gmail.com", password="super")
        self.super_user.save()
       
    def test_username_is_email(self):
        self.assertEqual(f'{self.base_user.get_username()}', self.email)
        self.assertEqual(
            f'{self.super_user.get_username()}', "super@gmail.com")
    
    def test_user_home_page(self):
        response = self.client.get(reverse('customuser:homepage'))
        self.assertEqual(response.status_code, 200)
    
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


    

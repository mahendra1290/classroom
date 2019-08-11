from django.test import TestCase
from .models import Teacher
from .models import TeachersClassRoom
from customuser.models import User
from django.urls import reverse

TEACHER = None


def create_teacher(name, email, password, department, phone):
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    user.is_active = True
    user.is_teacher = True
    user.save()
    teacher = Teacher(
        name=name,
        department=department,
        phone=phone,
        user=user,
    )
    teacher.save()
    return teacher

def create_classroom(title, section, subject, teacher):
    classroom = TeachersClassRoom(
        title=title,
        section=section,
        subject=subject,
        teacher=teacher
    )
    return classroom


class TeacherModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test_teacher@nitkkr.com",
            password="qaz"
        )
        self.user.is_active = True
        self.user.is_teacher = True
        self.user.save()
        self.teacher = Teacher(
            name='test teacher',
            department='CD',
            phone=9828127640,
            user=self.user
        )
        self.teacher.save()
        global TEACHER
        TEACHER = self.teacher

    def test_user(self):
        self.assertEqual(self.teacher.user, self.user)

    def test_teacher_content(self):
        self.assertEqual(f'{self.teacher.name}', 'test teacher')
        self.assertEqual(f'{self.teacher.department}', 'CD')
        self.assertEqual(f'{self.teacher.phone}', '9828127640')

    def test_teacher_login_view(self):
        has_logined = self.client.login(
            username=self.teacher.get_username(), password='qaz')
        self.assertEqual(has_logined, True)
        response = self.client.get(reverse('customuser:homepage'))
        self.assertRedirects(response, reverse('teacher:homepage'))
        response = self.client.get(reverse('teacher:homepage'))
        self.assertTemplateUsed(response, 'teacher_window.html')


class ClassroomModelTest(TestCase):

    def setUp(self):
        self.teacher = create_teacher(
            name="test_teacher",
            email="test_teacher@gmail.com",
            password="pass",
            department="CD",
            phone=9828127640
        )

        self.classroom_1 = create_classroom(
            title="classroom #1",
            section="section #1",
            subject="subject #1",
            teacher=self.teacher
        )

        def test_classroom_teacher(self):
            self.assertEqual(self.classroom_1.teacher, self.teacher)

class ClassRoomViewsTest(TestCase):
    pass

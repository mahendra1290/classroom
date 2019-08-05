from django.test import TestCase
from .models import Teacher
from .models import TeachersClassRoom
from customuser.models import User

TEACHER = None


def create_teacher(name, email, password, department, phone):
    base_user = User.objects.create_user(
        email=email,
        password=password,
    )
    teacher = Teacher(
        name=name,
        department=department,
        phone=phone,
        teacher_user=base_user,
    )
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
        self.base_user = User.objects.create_user(
            email="test_teacher@nitkkr.com",
            password="qaz"
        )
        self.base_user.is_teacher = True

        self.teacher = Teacher(
            name='test teacher',
            department='CD',
            phone=9828127640,
            teacher_user=self.base_user
        )
        global TEACHER
        TEACHER = self.teacher

    def test_base_user(self):
        self.assertEqual(self.teacher.teacher_user, self.base_user)

    def test_teacher_content(self):
        self.assertEqual(f'{self.teacher.name}', 'test teacher')
        self.assertEqual(f'{self.teacher.department}', 'CD')
        self.assertEqual(f'{self.teacher.phone}', '9828127640')


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

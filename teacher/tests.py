from django.test import TestCase
from .models import Teacher
from .models import TeachersClassRoom
from customuser.models import User


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
    
    def test_base_user(self):
        self.assertEqual(self.teacher.teacher_user, self.base_user)

    def test_teacher_content(self):
        self.assertEqual(f'{self.teacher.name}', 'test teacher')
        self.assertEqual(f'{self.teacher.department}', 'CD')
        self.assertEqual(f'{self.teacher.phone}', '9828127640')

    

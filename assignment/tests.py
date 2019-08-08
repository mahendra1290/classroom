from django.test import TestCase
from customuser.models import User
from teacher.models import Teacher
from teacher.models import TeachersClassRoom
from .models import Assignment
from .models import AssignmentsFile
from datetime import date


def create_teacher_user():
    base_user = User.objects.create_user(
        email="test_teacher@nitkkr.com",
        password="qaz"
    )
    base_user.teacher_status = True

    teacher = Teacher(
        name='test teacher',
        department='CD',
        phone=9828127640,
        teacher_user=base_user
    )
    return teacher


def create_classroom():
    teachers_classroom = TeachersClassRoom(
        title='test classroom', 
        section='test-section', 
        subject='test_suject',
        teacher=create_teacher_user()
    )
    return teachers_classroom


class AssignmentModelTest(TestCase):

    def setUp(self):
        self.class_room = create_classroom()
        self.test_assignment = Assignment(
            title='test assignment',
            instructions='no instructions',
            due_date=date.today(),
            pub_date=date.today(),
            assignment_of_class=self.class_room
        )
    
    def test_classroom(self):
        print(self.test_assignment.due_date)
        self.assertEqual(self.test_assignment.assignment_of_class, self.class_room)




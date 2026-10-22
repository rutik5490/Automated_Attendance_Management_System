import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Faculty, Dean, Student
from attendance.models import Class, Subject, StudentEnrollment, AttendanceRecord
from datetime import date, time

User = get_user_model()

def create_test_data():
    # Create users
    faculty_user = User.objects.create_user(
        username='faculty1',
        password='password123',
        user_type='faculty',
        whatsapp_number='+1234567890'
    )
    
    dean_user = User.objects.create_user(
        username='dean1',
        password='password123',
        user_type='dean',
        whatsapp_number='+1234567891'
    )
    
    student_user1 = User.objects.create_user(
        username='student1',
        password='password123',
        user_type='student',
        whatsapp_number='+1234567892'
    )
    
    student_user2 = User.objects.create_user(
        username='student2',
        password='password123',
        user_type='student',
        whatsapp_number='+1234567893'
    )
    
    # Create profiles
    faculty = Faculty.objects.create(
        user=faculty_user,
        name='Dr. Smith'
    )
    
    dean = Dean.objects.create(
        user=dean_user,
        name='Dr. Johnson'
    )
    
    student1 = Student.objects.create(
        user=student_user1,
        name='John Doe',
        roll_no='101',
        whatsapp_number='+1234567892'
    )
    
    student2 = Student.objects.create(
        user=student_user2,
        name='Jane Smith',
        roll_no='102',
        whatsapp_number='+1234567893'
    )
    
    # Create classes and subjects
    class_1 = Class.objects.create(
        name='Computer Science',
        year=2025,
        section='A'
    )
    
    subject_1 = Subject.objects.create(
        name='Python Programming',
        class_obj=class_1
    )
    
    # Enroll students
    enrollment1 = StudentEnrollment.objects.create(
        student=student1,
        class_obj=class_1
    )
    
    enrollment2 = StudentEnrollment.objects.create(
        student=student2,
        class_obj=class_1
    )
    
    # Create attendance records
    attendance1 = AttendanceRecord.objects.create(
        student=student1,
        subject=subject_1,
        date=date(2025, 10, 1),
        time=time(9, 0),
        status='present'
    )
    
    attendance2 = AttendanceRecord.objects.create(
        student=student2,
        subject=subject_1,
        date=date(2025, 10, 1),
        time=time(9, 0),
        status='absent'
    )
    
    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data()
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Student, Faculty, Dean
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users (students, faculty, deans) for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=10,
            help='Number of student users to create (default: 10)'
        )
        parser.add_argument(
            '--faculty',
            type=int,
            default=3,
            help='Number of faculty users to create (default: 3)'
        )
        parser.add_argument(
            '--deans',
            type=int,
            default=2,
            help='Number of dean users to create (default: 2)'
        )

    def handle(self, *args, **options):
        # Sample data
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'Christopher', 'Olivia', 'Matthew', 'Sophia', 
                      'Andrew', 'Isabella', 'Joshua', 'Mia', 'Daniel', 'Charlotte', 'James', 'Amelia', 'Robert', 'Harper']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

        # Create superuser if doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                user_type='admin',
                whatsapp_number='+1234567890'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser (admin/admin123)')
            )

        # Create students
        student_count = 0
        for i in range(options['students']):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'student{i+1:03d}'
            email = f'{username}@university.edu'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='student123',
                    first_name=first_name,
                    last_name=last_name,
                    user_type='student',
                    whatsapp_number=f'+12345678{i:02d}'
                )
                
                Student.objects.create(
                    user=user,
                    name=f'{first_name} {last_name}',
                    roll_no=f'{random.randint(1000, 9999)}',
                    whatsapp_number=f'+12345678{i:02d}'
                )
                student_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {student_count} student users')
        )

        # Create faculty
        faculty_count = 0
        for i in range(options['faculty']):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'faculty{i+1:02d}'
            email = f'{username}@university.edu'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='faculty123',
                    first_name=first_name,
                    last_name=last_name,
                    user_type='faculty',
                    whatsapp_number=f'+12345679{i:02d}'
                )
                
                Faculty.objects.create(
                    user=user,
                    name=f'Prof. {first_name} {last_name}'
                )
                faculty_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {faculty_count} faculty users')
        )

        # Create deans
        dean_count = 0
        for i in range(options['deans']):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'dean{i+1:02d}'
            email = f'{username}@university.edu'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='dean123',
                    first_name=first_name,
                    last_name=last_name,
                    user_type='dean',
                    whatsapp_number=f'+12345680{i:02d}'
                )
                
                Dean.objects.create(
                    user=user,
                    name=f'Dr. {first_name} {last_name}'
                )
                dean_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {dean_count} dean users')
        )

        self.stdout.write(
            self.style.SUCCESS('All sample users created successfully!')
        )
        self.stdout.write(
            self.style.NOTICE('Default passwords:')
        )
        self.stdout.write(
            self.style.NOTICE('- Students: student123')
        )
        self.stdout.write(
            self.style.NOTICE('- Faculty: faculty123')
        )
        self.stdout.write(
            self.style.NOTICE('- Deans: dean123')
        )
        self.stdout.write(
            self.style.NOTICE('- Admin: admin123')
        )
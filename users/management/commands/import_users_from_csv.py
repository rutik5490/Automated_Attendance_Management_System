import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Student, Faculty, Dean

User = get_user_model()

class Command(BaseCommand):
    help = 'Import users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
        parser.add_argument(
            '--type',
            type=str,
            choices=['student', 'faculty', 'dean'],
            required=True,
            help='Type of users to import'
        )

    def handle(self, *args, **options):
        if not os.path.exists(options['csv_file']):
            self.stdout.write(
                self.style.ERROR(f'CSV file {options["csv_file"]} does not exist')
            )
            return

        created_count = 0
        skipped_count = 0

        try:
            with open(options['csv_file'], 'r') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Extract common fields
                    username = row.get('username')
                    email = row.get('email')
                    first_name = row.get('first_name', '')
                    last_name = row.get('last_name', '')
                    whatsapp_number = row.get('whatsapp_number', '')
                    
                    # Check if user already exists
                    if User.objects.filter(username=username).exists():
                        self.stdout.write(
                            self.style.WARNING(f'User {username} already exists, skipping...')
                        )
                        skipped_count += 1
                        continue
                    
                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='default123',  # Default password, should be changed by user
                        first_name=first_name,
                        last_name=last_name,
                        user_type=options['type'],
                        whatsapp_number=whatsapp_number
                    )
                    
                    # Create profile based on user type
                    if options['type'] == 'student':
                        Student.objects.create(
                            user=user,
                            name=f'{first_name} {last_name}',
                            roll_no=row.get('roll_no', ''),
                            whatsapp_number=whatsapp_number
                        )
                    elif options['type'] == 'faculty':
                        Faculty.objects.create(
                            user=user,
                            name=f'Prof. {first_name} {last_name}' if first_name else username
                        )
                    elif options['type'] == 'dean':
                        Dean.objects.create(
                            user=user,
                            name=f'Dr. {first_name} {last_name}' if first_name else username
                        )
                    
                    created_count += 1

            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {created_count} {options["type"]} users')
            )
            if skipped_count > 0:
                self.stdout.write(
                    self.style.WARNING(f'Skipped {skipped_count} existing users')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing users: {str(e)}')
            )
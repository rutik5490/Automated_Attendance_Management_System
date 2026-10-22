from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Class, Subject, AttendanceRecord
from users.models import Student
import csv
import os

class Command(BaseCommand):
    help = 'Sync attendance data from external database or CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            help='Path to CSV file with attendance data',
        )
        parser.add_argument(
            '--external-db',
            type=str,
            help='Connection string for external database',
        )

    def handle(self, *args, **options):
        if options['csv_file']:
            self.sync_from_csv(options['csv_file'])
        elif options['external_db']:
            self.sync_from_external_db(options['external_db'])
        else:
            self.stdout.write(
                self.style.ERROR('Please provide either --csv-file or --external-db')
            )

    def sync_from_csv(self, csv_file_path):
        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR(f'CSV file {csv_file_path} does not exist')
            )
            return

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                success_count = 0
                error_count = 0

                for row in reader:
                    try:
                        # Extract data from CSV row
                        date_str = row.get('Date', '')
                        roll_no = row.get('Roll No', '')
                        subject_name = row.get('Subject', '')
                        status = row.get('Status', '').lower()

                        # Validate data
                        if not all([date_str, roll_no, subject_name, status]):
                            error_count += 1
                            continue

                        # Parse date
                        from datetime import datetime
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                        # Get student
                        try:
                            student = Student.objects.get(roll_no=roll_no)
                        except Student.DoesNotExist:
                            error_count += 1
                            continue

                        # Get subject
                        try:
                            subject = Subject.objects.get(name=subject_name)
                        except Subject.DoesNotExist:
                            error_count += 1
                            continue

                        # Create or update attendance record
                        attendance_record, created = AttendanceRecord.objects.get_or_create(
                            student=student,
                            subject=subject,
                            date=date_obj,
                            defaults={
                                'time': timezone.now().time(),
                                'status': status
                            }
                        )

                        if not created:
                            # Update existing record
                            attendance_record.status = status
                            attendance_record.time = timezone.now().time()
                            attendance_record.save()

                        success_count += 1

                    except Exception as e:
                        error_count += 1
                        continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully processed {success_count} records. {error_count} records failed.'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading CSV file: {str(e)}')
            )

    def sync_from_external_db(self, connection_string):
        # This is a placeholder for actual database connection logic
        # In a real implementation, you would connect to the external database
        # and fetch attendance data
        
        self.stdout.write(
            self.style.WARNING(
                'External database sync is not implemented in this example. '
                'This would require implementing actual database connection logic.'
            )
        )
        
        # Example of what the implementation might look like:
        # import psycopg2  # or another database adapter
        # conn = psycopg2.connect(connection_string)
        # cursor = conn.cursor()
        # cursor.execute("SELECT date, roll_no, subject, status FROM attendance_table")
        # records = cursor.fetchall()
        # Process records similar to CSV approach
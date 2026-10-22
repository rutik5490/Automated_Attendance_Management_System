from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Class, Subject, AttendanceRecord
from users.models import Student
import csv
import os

class Command(BaseCommand):
    help = 'Sync attendance data from institutional ERP system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--erp-csv',
            type=str,
            help='Path to ERP CSV export file',
        )
        parser.add_argument(
            '--erp-db',
            type=str,
            help='Connection string for ERP database',
        )

    def handle(self, *args, **options):
        if options['erp_csv']:
            self.sync_from_erp_csv(options['erp_csv'])
        elif options['erp_db']:
            self.sync_from_erp_database(options['erp_db'])
        else:
            self.stdout.write(
                self.style.ERROR('Please provide either --erp-csv or --erp-db')
            )

    def sync_from_erp_csv(self, csv_file_path):
        """
        Sync attendance data from ERP CSV export
        """
        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR(f'ERP CSV file {csv_file_path} does not exist')
            )
            return

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                success_count = 0
                error_count = 0

                for row in reader:
                    try:
                        # Extract data from ERP CSV row
                        # ERP systems typically have different column names
                        date_str = row.get('attendance_date', '') or row.get('date', '')
                        roll_no = row.get('student_roll_no', '') or row.get('roll_no', '')
                        subject_code = row.get('subject_code', '') or row.get('subject', '')
                        status = row.get('status', '').lower()

                        # Validate data
                        if not all([date_str, roll_no, subject_code, status]):
                            error_count += 1
                            continue

                        # Parse date
                        from datetime import datetime
                        # ERP systems might use different date formats
                        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
                        date_obj = None
                        
                        for fmt in date_formats:
                            try:
                                date_obj = datetime.strptime(date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        
                        if not date_obj:
                            error_count += 1
                            continue

                        # Get student
                        try:
                            student = Student.objects.get(roll_no=roll_no)
                        except Student.DoesNotExist:
                            error_count += 1
                            continue

                        # Get subject by code or name
                        try:
                            subject = Subject.objects.get(name__icontains=subject_code)
                        except Subject.DoesNotExist:
                            # Try to match by class if subject not found
                            try:
                                class_obj = Class.objects.first()  # Simplified - would need proper logic
                                subject = Subject.objects.filter(class_obj=class_obj).first()
                                if not subject:
                                    error_count += 1
                                    continue
                            except:
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
                        self.stdout.write(
                            self.style.WARNING(f'Error processing row: {str(e)}')
                        )
                        error_count += 1
                        continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully synced {success_count} records from ERP CSV. {error_count} records failed.'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading ERP CSV file: {str(e)}')
            )

    def sync_from_erp_database(self, connection_string):
        """
        Sync attendance data from ERP database
        This is a placeholder for actual database connection logic
        """
        self.stdout.write(
            self.style.WARNING(
                'ERP database sync is not implemented in this example. '
                'This would require implementing actual database connection logic '
                'based on your ERP system (e.g., MySQL, PostgreSQL, Oracle, etc.).'
            )
        )
        
        # Example of what the implementation might look like for different databases:
        
        # For MySQL:
        # import mysql.connector
        # conn = mysql.connector.connect(
        #     host='erp-host',
        #     user='erp-user',
        #     password='erp-password',
        #     database='erp-database'
        # )
        # cursor = conn.cursor()
        # cursor.execute("SELECT attendance_date, student_roll_no, subject_code, status FROM attendance_table")
        # records = cursor.fetchall()
        # Process records similar to CSV approach
        
        # For PostgreSQL:
        # import psycopg2
        # conn = psycopg2.connect(connection_string)
        # cursor = conn.cursor()
        # cursor.execute("SELECT attendance_date, student_roll_no, subject_code, status FROM attendance_table")
        # records = cursor.fetchall()
        # Process records similar to CSV approach
        
        # For Oracle:
        # import cx_Oracle
        # conn = cx_Oracle.connect(connection_string)
        # cursor = conn.cursor()
        # cursor.execute("SELECT attendance_date, student_roll_no, subject_code, status FROM attendance_table")
        # records = cursor.fetchall()
        # Process records similar to CSV approach
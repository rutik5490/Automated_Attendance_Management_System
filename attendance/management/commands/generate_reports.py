from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Class, Subject, AttendanceRecord
from users.models import Student
import csv
import os

class Command(BaseCommand):
    help = 'Generate attendance reports in various formats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            default='csv',
            choices=['csv', 'excel', 'pdf'],
            help='Report format (default: csv)',
        )
        parser.add_argument(
            '--output',
            type=str,
            default='attendance_report.csv',
            help='Output file path',
        )
        parser.add_argument(
            '--class-id',
            type=int,
            help='Class ID to generate report for',
        )

    def handle(self, *args, **options):
        format = options['format']
        output_path = options['output']
        class_id = options['class_id']

        if format == 'csv':
            self.generate_csv_report(output_path, class_id)
        elif format == 'excel':
            self.generate_excel_report(output_path, class_id)
        elif format == 'pdf':
            self.generate_pdf_report(output_path, class_id)

    def generate_csv_report(self, output_path, class_id=None):
        # Get attendance records
        if class_id:
            records = AttendanceRecord.objects.filter(subject__class_obj__id=class_id)
        else:
            records = AttendanceRecord.objects.all()

        # Write to CSV
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Student Name', 'Roll No', 'Class', 'Subject', 'Date', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in records:
                writer.writerow({
                    'Student Name': record.student.name,
                    'Roll No': record.student.roll_no,
                    'Class': record.subject.class_obj.name,
                    'Subject': record.subject.name,
                    'Date': record.date,
                    'Status': record.status,
                })

        self.stdout.write(
            self.style.SUCCESS(f'CSV report generated successfully: {output_path}')
        )

    def generate_excel_report(self, output_path, class_id=None):
        try:
            import openpyxl
        except ImportError:
            self.stdout.write(
                self.style.ERROR('openpyxl is required for Excel reports. Install it with: pip install openpyxl')
            )
            return

        # Get attendance records
        if class_id:
            records = AttendanceRecord.objects.filter(subject__class_obj__id=class_id)
        else:
            records = AttendanceRecord.objects.all()

        # Create workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Attendance Report'

        # Write headers
        headers = ['Student Name', 'Roll No', 'Class', 'Subject', 'Date', 'Status']
        sheet.append(headers)

        # Write data
        for record in records:
            sheet.append([
                record.student.name,
                record.student.roll_no,
                record.subject.class_obj.name,
                record.subject.name,
                record.date,
                record.status,
            ])

        # Save workbook
        workbook.save(output_path)

        self.stdout.write(
            self.style.SUCCESS(f'Excel report generated successfully: {output_path}')
        )

    def generate_pdf_report(self, output_path, class_id=None):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            self.stdout.write(
                self.style.ERROR('reportlab is required for PDF reports. Install it with: pip install reportlab')
            )
            return

        # Get attendance records
        if class_id:
            records = AttendanceRecord.objects.filter(subject__class_obj__id=class_id)
        else:
            records = AttendanceRecord.objects.all()

        # Create PDF
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Write title
        c.drawString(100, height - 50, "Attendance Report")

        # Write headers
        headers = ['Student Name', 'Roll No', 'Class', 'Subject', 'Date', 'Status']
        y = height - 100
        for i, header in enumerate(headers):
            c.drawString(100 + i * 80, y, header)

        # Write data
        y -= 20
        for record in records:
            if y < 50:  # New page if needed
                c.showPage()
                y = height - 50

            data = [
                record.student.name,
                record.student.roll_no,
                record.subject.class_obj.name,
                record.subject.name,
                str(record.date),
                record.status,
            ]

            for i, value in enumerate(data):
                c.drawString(100 + i * 80, y, value)

            y -= 20

        c.save()

        self.stdout.write(
            self.style.SUCCESS(f'PDF report generated successfully: {output_path}')
        )
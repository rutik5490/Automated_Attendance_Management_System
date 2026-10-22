from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Student
from attendance.models import AttendanceRecord
from notifications.models import WhatsAppMessage
import os

class Command(BaseCommand):
    help = 'Check student attendance and send WhatsApp alerts for those below 75%'

    def handle(self, *args, **options):
        # Get all students
        students = Student.objects.all()
        alert_count = 0
        
        for student in students:
            # Calculate attendance percentage
            total_classes = AttendanceRecord.objects.filter(student=student).count()
            
            if total_classes == 0:
                continue
                
            present_classes = AttendanceRecord.objects.filter(
                student=student, 
                status='present'
            ).count()
            
            attendance_percentage = (present_classes / total_classes) * 100
            
            # Send alert if attendance is below 75%
            if attendance_percentage < 75:
                # Create WhatsApp message
                message_content = f"Dear {student.name}, your attendance is currently {attendance_percentage:.2f}%, which is below the required 75%. Please attend classes regularly."
                
                # Send actual WhatsApp message
                success = self.send_whatsapp_message(student.whatsapp_number, message_content)
                
                # Record the message regardless of delivery success
                WhatsAppMessage.objects.create(
                    student=student,
                    message=message_content,
                    is_delivered=success
                )
                
                if success:
                    alert_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sent low attendance alerts to {alert_count} students'
            )
        )

    def send_whatsapp_message(self, to_number, message):
        """
        Send WhatsApp message using Twilio API
        """
        try:
            from twilio.rest import Client
            
            # Get credentials from environment variables
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
            
            # Check if credentials are available
            if not all([account_sid, auth_token, from_number]):
                self.stdout.write(
                    self.style.WARNING(
                        'Twilio credentials not configured. Skipping actual message sending.'
                    )
                )
                return False
            
            # Create Twilio client
            client = Client(account_sid, auth_token)
            
            # Send message
            message = client.messages.create(
                from_=f'whatsapp:{from_number}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to send WhatsApp message: {str(e)}'
                )
            )
            return False
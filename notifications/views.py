from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WhatsAppMessage
from users.models import Student
from attendance.models import AttendanceRecord

# Create your views here.

@login_required
def send_custom_whatsapp_message(request):
    if request.user.user_type != 'faculty':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        # In a real implementation, this would integrate with a WhatsApp API
        # For now, we'll just simulate the functionality
        student_id = request.POST.get('student_id')
        message_content = request.POST.get('message')
        
        try:
            student = Student.objects.get(id=student_id)
            
            # Create a WhatsApp message record
            whatsapp_message = WhatsAppMessage.objects.create(
                student=student,
                message=message_content,
                is_delivered=True  # Simulate successful delivery
            )
            
            messages.success(request, f'Message sent to {student.name}')
        except Student.DoesNotExist:
            messages.error(request, 'Student not found')
        
        return redirect('faculty_dashboard')
    
    # For GET request, show the message form
    students = Student.objects.all()
    return render(request, 'notifications/send_message.html', {'students': students})

def calculate_attendance_percentage(student):
    """
    Calculate attendance percentage for a student
    """
    total_classes = AttendanceRecord.objects.filter(student=student).count()
    if total_classes == 0:
        return 0
    
    present_classes = AttendanceRecord.objects.filter(
        student=student, 
        status='present'
    ).count()
    
    return (present_classes / total_classes) * 100

def check_and_send_low_attendance_alerts():
    """
    Check all students' attendance and send alerts for those below 75%
    This would typically be run as a scheduled task
    """
    students = Student.objects.all()
    
    for student in students:
        attendance_percentage = calculate_attendance_percentage(student)
        
        if attendance_percentage < 75:
            # Send WhatsApp alert to student
            message_content = f"Dear {student.name}, your attendance is currently {attendance_percentage:.2f}%, which is below the required 75%. Please attend classes regularly."
            
            WhatsAppMessage.objects.create(
                student=student,
                message=message_content,
                is_delivered=True  # Simulate successful delivery
            )
            
            # In a real implementation, you would also send to parent
            # and use an actual WhatsApp API
            
    return f"Checked {len(students)} students. Alerts sent where necessary."
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
import json
from .models import AttendanceRecord, Class, Subject
from users.models import Student

@login_required
def upload_attendance_csv(request):
    """Handle CSV upload for attendance records"""
    if request.method == 'POST':
        # In a real implementation, this would process the uploaded CSV file
        messages.success(request, 'Attendance CSV uploaded successfully')
        return redirect('faculty_dashboard')
    
    return render(request, 'attendance/upload_csv.html')

@login_required
def generate_attendance_report(request):
    """Generate attendance reports"""
    # In a real implementation, this would generate reports
    messages.success(request, 'Attendance report generated successfully')
    return redirect('faculty_dashboard')

class RaspberryPiAttendanceView(View):
    """API endpoint for Raspberry Pi attendance submission"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            subject_id = data.get('subject_id')
            status = data.get('status', 'present')
            
            # Validate and create attendance record
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            
            attendance_record = AttendanceRecord.objects.create(
                student=student,
                subject=subject,
                date=timezone.now().date(),
                time=timezone.now().time(),
                status=status
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Attendance recorded successfully',
                'record_id': attendance_record.id
            })
            
        except Student.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Student not found'
            }, status=404)
            
        except Subject.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Subject not found'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
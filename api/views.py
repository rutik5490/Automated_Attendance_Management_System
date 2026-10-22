from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.models import Student
from attendance.models import AttendanceRecord, Class, Subject

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_attendance_summary(request):
    """Get attendance summary for the authenticated student"""
    try:
        student = Student.objects.get(user=request.user)
        attendance_percentage = student.attendance_percentage()
        
        return Response({
            'student_name': student.name,
            'roll_no': student.roll_no,
            'attendance_percentage': attendance_percentage,
            'status': 'success'
        })
    except Student.DoesNotExist:
        return Response({
            'error': 'Student profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    """API endpoint for marking attendance (for faculty)"""
    # This would require additional permissions and validation
    # Implementation details would depend on specific requirements
    return Response({
        'message': 'Attendance marking endpoint'
    })
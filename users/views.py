from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User, Faculty, Dean, Student

# Create your views here.

def is_faculty(user):
    return user.user_type == 'faculty'

def is_dean(user):
    return user.user_type == 'dean'

def is_student(user):
    return user.user_type == 'student'

def is_admin(user):
    return user.is_staff and user.is_superuser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if is_admin(user):
                return redirect('/admin/')
            elif is_faculty(user):
                return redirect('faculty_dashboard')
            elif is_dean(user):
                return redirect('dean_dashboard')
            elif is_student(user):
                return redirect('student_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    # If user is authenticated, redirect to their dashboard
    if request.user.is_authenticated:
        # Handle admin/superuser users
        if is_admin(request.user):
            return redirect('/admin/')
        elif hasattr(request.user, 'user_type'):
            if is_faculty(request.user):
                return redirect('faculty_dashboard')
            elif is_dean(request.user):
                return redirect('dean_dashboard')
            elif is_student(request.user):
                return redirect('student_dashboard')
    
    # If not authenticated, show the home page with login option
    return render(request, 'users/home.html')

@login_required
@user_passes_test(is_faculty, login_url='login')
def faculty_dashboard(request):
    # Get faculty-specific data
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        faculty = None
    
    context = {
        'faculty': faculty,
    }
    return render(request, 'users/faculty_dashboard.html', context)

@login_required
@user_passes_test(is_dean, login_url='login')
def dean_dashboard(request):
    # Get dean-specific data with optimized queries
    try:
        dean = Dean.objects.select_related('user').get(user=request.user)
    except Dean.DoesNotExist:
        dean = None
    
    # Get attendance statistics with optimized queries
    from attendance.models import AttendanceRecord, Class
    from django.db.models import Count
    
    total_students = Student.objects.count()
    total_attendance_records = AttendanceRecord.objects.count()
    
    # Get class-wise attendance statistics with optimized queries
    class_stats = Class.objects.prefetch_related('subjects').annotate(
        total_students=Count('subjects__attendancerecord__student', distinct=True),
        total_records=Count('subjects__attendancerecord')
    )
    
    context = {
        'dean': dean,
        'total_students': total_students,
        'total_attendance_records': total_attendance_records,
        'class_stats': class_stats,
    }
    return render(request, 'users/dean_dashboard.html', context)

@login_required
@user_passes_test(is_student, login_url='login')
def student_dashboard(request):
    # Get student-specific data
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None
    
    # Calculate attendance percentage using model method
    if student:
        from attendance_system.settings import MIN_ATTENDANCE_PERCENTAGE
        attendance_percentage = student.attendance_percentage()
        low_attendance = attendance_percentage < MIN_ATTENDANCE_PERCENTAGE
        
        context = {
            'student': student,
            'attendance_percentage': attendance_percentage,
            'low_attendance': low_attendance,
            'min_attendance': MIN_ATTENDANCE_PERCENTAGE,
        }
    else:
        context = {
            'student': student,
        }
    
    return render(request, 'users/student_dashboard.html', context)
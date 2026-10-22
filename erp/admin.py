from django.contrib import admin
from .models import Department, Course, Semester, Classroom, Schedule, Enrollment, Resource, ResourceBooking

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head')
    search_fields = ('name', 'code')
    list_filter = ('head',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credits')
    search_fields = ('code', 'name')
    list_filter = ('department', 'credits')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('building', 'room_number', 'capacity')
    search_fields = ('building', 'room_number')
    list_filter = ('building',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'faculty', 'classroom', 'day_of_week', 'start_time', 'end_time')
    search_fields = ('course__name', 'faculty__name')
    list_filter = ('day_of_week', 'classroom', 'semester')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'enrollment_date', 'grade')
    search_fields = ('student__name', 'course__name')
    list_filter = ('semester', 'course')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'quantity', 'available_quantity')
    search_fields = ('name',)
    list_filter = ('resource_type',)

@admin.register(ResourceBooking)
class ResourceBookingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'booked_by', 'start_datetime', 'end_datetime', 'is_approved')
    search_fields = ('resource__name', 'booked_by__name')
    list_filter = ('is_approved', 'start_datetime')
from django.contrib import admin
from .models import Class, Subject, StudentEnrollment, AttendanceRecord

# Register your models here.

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'section', 'total_students')
    list_filter = ('year', 'section')
    search_fields = ('name', 'section')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_obj')
    list_filter = ('class_obj__year', 'class_obj__name')
    search_fields = ('name',)

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj')
    list_filter = ('class_obj__name', 'class_obj__year')
    search_fields = ('student__name', 'student__roll_no')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'time')
    list_filter = ('status', 'date', 'subject__class_obj__name', 'subject__name')
    search_fields = ('student__name', 'student__roll_no', 'subject__name')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    
    # Prevent editing past records
    def has_change_permission(self, request, obj=None):
        if obj and obj.date < timezone.now().date():
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.date < timezone.now().date():
            return False
        return super().has_delete_permission(request, obj)
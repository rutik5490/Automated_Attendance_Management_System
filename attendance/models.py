from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import Student, Faculty

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} {self.year} {self.section}"
    
    def total_students(self):
        """Get total number of students enrolled in this class"""
        return self.studentenrollment_set.count()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        return f"{self.name} - {self.class_obj.name}"
    
    class Meta:
        verbose_name_plural = "Subjects"

class StudentEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student.name} in {self.class_obj.name}"
    
    class Meta:
        unique_together = ('student', 'class_obj')

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Check if the record is for a past date and prevent editing
        if self.pk and self.date < timezone.now().date():
            # Get the original record from database
            original = AttendanceRecord.objects.get(pk=self.pk)
            if (self.student != original.student or 
                self.subject != original.subject or 
                self.date != original.date or 
                self.status != original.status):
                raise ValidationError("Cannot modify past attendance records.")
    
    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date} - {self.status}"
    
    @classmethod
    def get_student_attendance_percentage(cls, student, subject=None):
        """Get attendance percentage for a student, optionally filtered by subject"""
        queryset = cls.objects.filter(student=student)
        if subject:
            queryset = queryset.filter(subject=subject)
        
        total = queryset.count()
        if total == 0:
            return 0
        
        present = queryset.filter(status='present').count()
        return round((present / total) * 100, 2)
    
    @classmethod
    def get_class_attendance_report(cls, class_obj):
        """Get attendance report for all students in a class"""
        from django.db.models import Count
        return cls.objects.filter(
            subject__class_obj=class_obj
        ).values(
            'student__name',
            'student__roll_no'
        ).annotate(
            total_classes=Count('id'),
            present_classes=Count('id', filter=models.Q(status='present')),
        ).annotate(
            percentage=models.ExpressionWrapper(
                models.F('present_classes') * 100.0 / models.F('total_classes'),
                output_field=models.FloatField()
            )
        )
    
    class Meta:
        unique_together = ('student', 'subject', 'date')
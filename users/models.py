from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('faculty', 'Faculty'),
        ('dean', 'Dean'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Dean(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    whatsapp_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    def attendance_percentage(self):
        """Calculate overall attendance percentage"""
        from attendance.models import AttendanceRecord
        total_records = AttendanceRecord.objects.filter(student=self).count()
        if total_records == 0:
            return 0
        present_records = AttendanceRecord.objects.filter(
            student=self, 
            status='present'
        ).count()
        return round((present_records / total_records) * 100, 2)
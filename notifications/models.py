from django.db import models
from users.models import Student
from attendance.models import AttendanceRecord

# Create your models here.

class WhatsAppMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"WhatsApp to {self.student.name} at {self.sent_at}"

class AttendanceAlert(models.Model):
    ALERT_TYPES = (
        ('low_attendance', 'Low Attendance'),
        ('improvement', 'Attendance Improvement'),
        ('warning', 'Attendance Warning'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    sent_via = models.CharField(max_length=20, default='email')  # email, sms, whatsapp
    
    def __str__(self):
        return f"{self.get_alert_type_display()} alert for {self.student.name}"
    
    class Meta:
        ordering = ['-created_at']
from django.db import models
from users.models import Faculty, Student

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.IntegerField()
    description = models.TextField(blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Semester(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Classroom(models.Model):
    building = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    equipment = models.TextField(blank=True, help_text="List of equipment available in the classroom")
    
    class Meta:
        unique_together = ('building', 'room_number')
    
    def __str__(self):
        return f"{self.building} - {self.room_number}"

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.course.code} - {self.day_of_week} {self.start_time}-{self.end_time}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True)
    
    class Meta:
        unique_together = ('student', 'course', 'semester')
    
    def __str__(self):
        return f"{self.student.name} - {self.course.code}"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('EQUIPMENT', 'Equipment'),
        ('SOFTWARE', 'Software'),
        ('ROOM', 'Room'),
        ('VEHICLE', 'Vehicle'),
    ]
    
    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.resource_type})"

class ResourceBooking(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    purpose = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.resource.name} - {self.booked_by.name}"
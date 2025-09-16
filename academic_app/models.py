from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        help_text="Course name (e.g., 'Advanced Mathematics')"
    )
    code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Course code (e.g., 'MATH301')"
    )
    instructor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Instructor name"
    )
    credits = models.PositiveIntegerField(
        default=3,
        help_text="Number of credit hours"
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Color for calendar display (hex code)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'code']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class Assignment(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        help_text="Assignment title"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Assignment description or instructions"
    )
    due_date = models.DateTimeField(help_text="Due date and time")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Priority level"
    )
    completed = models.BooleanField(default=False)
    estimated_hours = models.PositiveIntegerField(
        default=1,
        help_text="Estimated time to complete (hours)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'priority']
    
    def __str__(self):
        return f"{self.title} ({self.course.name})"
    
    @property
    def is_overdue(self):
        return self.due_date < timezone.now() and not self.completed


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        help_text="Exam title"
    )
    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE_CHOICES,
        default='midterm',
        help_text="Type of exam"
    )
    exam_date = models.DateTimeField(help_text="Exam date and time")
    duration = models.PositiveIntegerField(
        default=120,
        help_text="Duration in minutes"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Exam location"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or topics to study"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['exam_date']
    
    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(help_text="Class date")
    present = models.BooleanField(default=True, help_text="Present or absent")
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the class"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'date']
        ordering = ['-date']
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.course.name} - {self.date} - {status}"


class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('academic', 'Academic'),
        ('social', 'Social'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calendar_events")
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        help_text="Event title"
    )
    event_date = models.DateTimeField(help_text="Event date and time")
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Event end time (optional)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Event description"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='personal',
        help_text="Type of event"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Event location"
    )
    color = models.CharField(
        max_length=7,
        default="#28a745",
        help_text="Color for calendar display (hex code)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.title} ({self.event_date})"


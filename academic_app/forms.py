from django import forms
from django.contrib.auth.models import User
from .models import Course, Assignment, Exam, Attendance, CalendarEvent
from django.utils import timezone

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "instructor", "credits", "color"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., Advanced Mathematics"
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., MATH301"
            }),
            "instructor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Professor Name"
            }),
            "credits": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 6
            }),
            "color": forms.TextInput(attrs={
                "class": "form-control",
                "type": "color"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Note: self.user is not needed here as it's not used in this form.
        # But including it prevents the TypeError.

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "due_date", "priority", "estimated_hours"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Assignment title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Assignment description (optional)"
            }),
            "due_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "priority": forms.Select(attrs={
                "class": "form-select"
            }),
            "estimated_hours": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 100
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['course'].widget.attrs.update({"class": "form-select"})

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["course", "title", "exam_type", "exam_date", "duration", "location", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Exam title"
            }),
            "exam_type": forms.Select(attrs={
                "class": "form-select"
            }),
            "exam_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 15,
                "max": 480,
                "placeholder": "Duration in minutes"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Exam location (optional)"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Study notes or topics (optional)"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['course'].widget.attrs.update({"class": "form-select"})

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["course", "date", "present", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "present": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Notes about the class (optional)"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['course'].widget.attrs.update({"class": "form-select"})

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ["title", "event_date", "end_date", "description", "event_type", "location", "color"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event title"
            }),
            "event_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "end_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Event description (optional)"
            }),
            "event_type": forms.Select(attrs={
                "class": "form-select"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event location (optional)"
            }),
            "color": forms.TextInput(attrs={
                "class": "form-control",
                "type": "color"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Note: self.user is not needed here as it's not used in this form.
        # But including it prevents the TypeError.

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and event_date and end_date <= event_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data

class AssignmentEditForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date", "priority", "estimated_hours", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "estimated_hours": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
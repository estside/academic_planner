# academic_app/agent.py

from .models import Course, Assignment, Exam
from django.utils import timezone

class AcademicAgent:
    def add_assignment(self, course_name, title, due_date):
        try:
            course = Course.objects.get(name=course_name)
            Assignment.objects.create(course=course, title=title, due_date=due_date)
            return f"Successfully added '{title}' to {course_name}."
        except Course.DoesNotExist:
            return f"Error: Course '{course_name}' not found."

    def get_upcoming_deadlines(self):
        # Retrieve all upcoming assignments and exams
        now = timezone.now()
        upcoming_assignments = Assignment.objects.filter(due_date__gte=now).order_by('due_date')
        upcoming_exams = Exam.objects.filter(exam_date__gte=now).order_by('exam_date')
        
        # Format the output for the user
        response = "Your upcoming deadlines are:\n"
        if not upcoming_assignments and not upcoming_exams:
            response += "No upcoming deadlines found."
        
        for assignment in upcoming_assignments:
            response += f"- Assignment: {assignment.title} (Course: {assignment.course.name}, Due: {assignment.due_date})\n"
        
        for exam in upcoming_exams:
            response += f"- Exam: {exam.title} (Course: {exam.course.name}, Date: {exam.exam_date})\n"

        return response

# ... (add more methods for other tasks)
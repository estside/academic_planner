# gemini_agent_app/tools.py
from academic_app.models import Course, Assignment, Exam, CalendarEvent, Attendance
from django.db.models import F
from django.contrib.auth.models import User
from datetime import datetime
import json

def get_academic_summary(user_id: int):
    """
    Retrieves all courses, assignments, and exams for a specific user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        A formatted string summary of all academic data.
    """
    try:
        user = User.objects.get(id=user_id)
        courses = user.courses.all()
        
        summary = "Here is your current academic data:\n\n"
        
        if courses.exists():
            summary += "📚 **My Courses:**\n"
            for course in courses:
                summary += f"- **{course.name}** ({course.code})\n"
                summary += f"  👨‍🏫 Instructor: {course.instructor or 'Not specified'}\n"
                summary += f"  🎓 Credits: {course.credits}\n\n"
            
            # Get all assignments for user's courses
            assignments = Assignment.objects.filter(course__user=user).order_by('due_date')
            if assignments.exists():
                summary += "📝 **My Assignments:**\n"
                for assignment in assignments:
                    status = "✅ Completed" if assignment.completed else "⏰ Pending"
                    priority_emoji = {
                        'low': '🟢',
                        'medium': '🟡', 
                        'high': '🟠',
                        'urgent': '🔴'
                    }.get(assignment.priority, '🟡')
                    
                    summary += f"- **{assignment.title}** ({priority_emoji} {assignment.priority.title()})\n"
                    summary += f"  📚 Course: {assignment.course.name}\n"
                    summary += f"  📅 Due: {assignment.due_date.strftime('%B %d, %Y at %I:%M %p')}\n"
                    summary += f"  ⏱️ Status: {status}\n"
                    if assignment.description:
                        summary += f"  📄 Description: {assignment.description[:100]}{'...' if len(assignment.description) > 100 else ''}\n"
                    summary += "\n"
            
            # Get all exams for user's courses
            exams = Exam.objects.filter(course__user=user).order_by('exam_date')
            if exams.exists():
                summary += "📋 **My Exams:**\n"
                for exam in exams:
                    exam_type_emoji = {
                        'midterm': '📝',
                        'final': '🏆',
                        'quiz': '✏️',
                        'project': '📊',
                        'presentation': '🎤'
                    }.get(exam.exam_type, '📝')
                    
                    summary += f"- **{exam.title}** ({exam_type_emoji} {exam.exam_type.title()})\n"
                    summary += f"  📚 Course: {exam.course.name}\n"
                    summary += f"  📅 Date: {exam.exam_date.strftime('%B %d, %Y at %I:%M %p')}\n"
                    summary += f"  ⏱️ Duration: {exam.duration} minutes\n"
                    if exam.location:
                        summary += f"  📍 Location: {exam.location}\n"
                    if exam.notes:
                        summary += f"  📄 Notes: {exam.notes[:100]}{'...' if len(exam.notes) > 100 else ''}\n"
                    summary += "\n"
            
            # Get recent attendance records
            attendance_records = Attendance.objects.filter(course__user=user).order_by('-date')[:5]
            if attendance_records.exists():
                summary += "✅ **Recent Attendance:**\n"
                for record in attendance_records:
                    status = "✅ Present" if record.present else "❌ Absent"
                    summary += f"- **{record.course.name}** - {record.date.strftime('%B %d, %Y')}: {status}\n"
                summary += "\n"
            
            # Get upcoming events
            from datetime import datetime, timedelta
            upcoming_events = CalendarEvent.objects.filter(
                user=user,
                event_date__gte=datetime.now(),
                event_date__lte=datetime.now() + timedelta(days=14)
            ).order_by('event_date')
            
            if upcoming_events.exists():
                summary += "📅 **Upcoming Events (Next 14 Days):**\n"
                for event in upcoming_events:
                    event_type_emoji = {
                        'personal': '👤',
                        'academic': '🎓',
                        'social': '👥',
                        'other': '📅'
                    }.get(event.event_type, '📅')
                    
                    summary += f"- **{event.title}** ({event_type_emoji})\n"
                    summary += f"  📅 Date: {event.event_date.strftime('%B %d, %Y at %I:%M %p')}\n"
                    if event.location:
                        summary += f"  📍 Location: {event.location}\n"
                    if event.description:
                        summary += f"  📄 Description: {event.description[:100]}{'...' if len(event.description) > 100 else ''}\n"
                    summary += "\n"
        else:
            summary += "📚 **No courses found.** You can add courses by saying something like:\n"
            summary += "- 'Add a course called Advanced Mathematics with code MATH301 taught by Dr. Smith'\n"
            summary += "- 'I want to add Computer Science 101 taught by Professor Johnson'\n\n"
        
        return summary
        
    except User.DoesNotExist:
        return "❌ User not found. Please make sure you're logged in."
    except Exception as e:
        return f"❌ Error retrieving your academic data: {str(e)}\n\nPlease try again or contact support if the problem persists."

def add_new_course(user_id: int, name: str, code: str, instructor: str):
    """
    Adds a new course to the user's database.
    Args:
        user_id (int): The ID of the user.
        name (str): The name of the course.
        code (str): The course code.
        instructor (str): The name of the instructor.
    Returns:
        A success message or an error string.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Check if course with same code already exists for this user
        if Course.objects.filter(user=user, code=code).exists():
            return f"❌ A course with code '{code}' already exists. Please use a different code."
        
        # Create the course with default values for new fields
        course = Course.objects.create(
            user=user, 
            name=name, 
            code=code, 
            instructor=instructor,
            credits=3,  # Default to 3 credits
            color="#007bff"  # Default blue color
        )
        
        return f"✅ Successfully added the course '{name}' ({code}) taught by {instructor} to your list! 🎓"
        
    except User.DoesNotExist:
        return "❌ User not found. Please make sure you're logged in."
    except Exception as e:
        return f"❌ Error adding course: {str(e)}"
    

def add_calendar_event(user_id: int, title: str, event_date: str, description: str = ""):
    """
    Adds a new calendar event to the user's database.
    Args:
        user_id (int): The ID of the user.
        title (str): The title of the event.
        event_date (str): The date and time of the event in ISO format (YYYY-MM-DDTHH:MM:SS).
        description (str): A description of the event.
    Returns:
        A success message or an error string.
    """
    try:
        user = User.objects.get(id=user_id)
        # Convert the string date to a datetime object
        event_datetime = datetime.fromisoformat(event_date)
        
        # Create the event with default values for new fields
        event = CalendarEvent.objects.create(
            user=user, 
            title=title, 
            event_date=event_datetime, 
            description=description,
            event_type='personal',  # Default to personal event
            color="#28a745"  # Default green color
        )
        
        return f"✅ Successfully added '{title}' to your calendar for {event_datetime.strftime('%B %d, %Y at %I:%M %p')}! 📅"
        
    except User.DoesNotExist:
        return "❌ User not found. Please make sure you're logged in."
    except ValueError:
        return "❌ Invalid date format. Please use YYYY-MM-DDTHH:MM:SS format."
    except Exception as e:
        return f"❌ Error adding calendar event: {str(e)}"


def add_assignment(user_id: int, course_code: str, title: str, due_date: str, priority: str = "medium", description: str = ""):
    """
    Adds a new assignment to a specific course.
    Args:
        user_id (int): The ID of the user.
        course_code (str): The code of the course.
        title (str): The title of the assignment.
        due_date (str): The due date in ISO format (YYYY-MM-DDTHH:MM:SS).
        priority (str): The priority level (low, medium, high, urgent).
        description (str): A description of the assignment.
    Returns:
        A success message or an error string.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Find the course by code
        try:
            course = Course.objects.get(user=user, code=course_code)
        except Course.DoesNotExist:
            return f"❌ Course with code '{course_code}' not found. Please check the course code or add the course first."
        
        # Convert the string date to a datetime object
        due_datetime = datetime.fromisoformat(due_date)
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if priority.lower() not in valid_priorities:
            priority = 'medium'
        
        # Create the assignment
        assignment = Assignment.objects.create(
            course=course,
            title=title,
            due_date=due_datetime,
            priority=priority.lower(),
            description=description,
            estimated_hours=2  # Default estimate
        )
        
        return f"✅ Successfully added assignment '{title}' to {course.name} due on {due_datetime.strftime('%B %d, %Y at %I:%M %p')}! 📝"
        
    except User.DoesNotExist:
        return "❌ User not found. Please make sure you're logged in."
    except ValueError:
        return "❌ Invalid date format. Please use YYYY-MM-DDTHH:MM:SS format."
    except Exception as e:
        return f"❌ Error adding assignment: {str(e)}"


def add_exam(user_id: int, course_code: str, title: str, exam_date: str, exam_type: str = "midterm", duration: int = 120, location: str = ""):
    """
    Adds a new exam to a specific course.
    Args:
        user_id (int): The ID of the user.
        course_code (str): The code of the course.
        title (str): The title of the exam.
        exam_date (str): The exam date in ISO format (YYYY-MM-DDTHH:MM:SS).
        exam_type (str): The type of exam (midterm, final, quiz, project, presentation).
        duration (int): The duration in minutes.
        location (str): The exam location.
    Returns:
        A success message or an error string.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Find the course by code
        try:
            course = Course.objects.get(user=user, code=course_code)
        except Course.DoesNotExist:
            return f"❌ Course with code '{course_code}' not found. Please check the course code or add the course first."
        
        # Convert the string date to a datetime object
        exam_datetime = datetime.fromisoformat(exam_date)
        
        # Validate exam type
        valid_types = ['midterm', 'final', 'quiz', 'project', 'presentation']
        if exam_type.lower() not in valid_types:
            exam_type = 'midterm'
        
        # Create the exam
        exam = Exam.objects.create(
            course=course,
            title=title,
            exam_date=exam_datetime,
            exam_type=exam_type.lower(),
            duration=duration,
            location=location
        )
        
        return f"✅ Successfully added {exam_type} exam '{title}' for {course.name} on {exam_datetime.strftime('%B %d, %Y at %I:%M %p')}! 📋"
        
    except User.DoesNotExist:
        return "❌ User not found. Please make sure you're logged in."
    except ValueError:
        return "❌ Invalid date format. Please use YYYY-MM-DDTHH:MM:SS format."
    except Exception as e:
        return f"❌ Error adding exam: {str(e)}"
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from .models import Course, Assignment, Exam, Attendance, CalendarEvent
from .forms import CourseForm, AssignmentForm, ExamForm, AttendanceForm, CalendarEventForm, AssignmentEditForm
import json


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to your academic planner.")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    user_courses = Course.objects.filter(user=request.user)
    
    # Initialize all forms here, so they are always defined for both GET and POST requests
    course_form = CourseForm(user=request.user)
    assignment_form = AssignmentForm(user=request.user)
    exam_form = ExamForm(user=request.user)
    event_form = CalendarEventForm(user=request.user)

    # Handle form submissions
    if request.method == "POST":
        # Check if this is an AJAX request
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        print(f"POST request received. AJAX: {is_ajax}")
        print(f"POST data: {request.POST}")
        
        # Use a hidden field in the form to determine which form was submitted.
        # This is a robust way to handle multiple forms on one page.
        if "course-submit" in request.POST:
            form = CourseForm(request.POST, user=request.user)
            if form.is_valid():
                course = form.save(commit=False)
                course.user = request.user
                course.save()
                messages.success(request, f"Course '{course.name}' added successfully!")
                
                # Handle AJAX requests
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': f"Course '{course.name}' added successfully!"
                    })
                
                return redirect("dashboard")
            else:
                messages.error(request, "Please correct the course form errors.")
                print(f"Course form errors: {form.errors}")
                
                # Handle AJAX requests with errors
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please correct the course form errors.',
                        'errors': form.errors
                    })
                
                course_form = form  # Re-assign the form with errors
        
        elif "assignment-submit" in request.POST:
            print("Processing assignment submission...")
            print(f"Course ID from POST: {request.POST.get('course')}")
            print(f"User courses: {list(Course.objects.filter(user=request.user).values_list('id', 'name'))}")
            form = AssignmentForm(request.POST, user=request.user)
            print(f"Form is valid: {form.is_valid()}")
            if not form.is_valid():
                print(f"Form errors: {form.errors}")
                print(f"Form non_field_errors: {form.non_field_errors()}")
                print(f"Form cleaned_data: {form.cleaned_data if hasattr(form, 'cleaned_data') else 'No cleaned_data'}")
            
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.save()
                print(f"Assignment saved: {assignment.title}")
                messages.success(request, f"Assignment '{assignment.title}' added successfully!")
                
                # Handle AJAX requests
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': f"Assignment '{assignment.title}' added successfully!"
                    })
                
                return redirect("dashboard")
            else:
                messages.error(request, "Please correct the assignment form errors.")
                print(f"Assignment form errors: {form.errors}")
                
                # Handle AJAX requests with errors
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please correct the assignment form errors.',
                        'errors': dict(form.errors)
                    })
                
                assignment_form = form # Re-assign the form with errors

        elif "exam-submit" in request.POST:
            form = ExamForm(request.POST, user=request.user)
            if form.is_valid():
                exam = form.save()
                messages.success(request, f"Exam '{exam.title}' added successfully!")
                
                # Handle AJAX requests
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': f"Exam '{exam.title}' added successfully!"
                    })
                
                return redirect("dashboard")
            else:
                messages.error(request, "Please correct the exam form errors.")
                print(f"Exam form errors: {form.errors}")
                
                # Handle AJAX requests with errors
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please correct the exam form errors.',
                        'errors': dict(form.errors)
                    })
                
                exam_form = form # Re-assign the form with errors

        elif "event-submit" in request.POST:
            form = CalendarEventForm(request.POST, user=request.user)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                messages.success(request, f"Event '{event.title}' added successfully!")
                
                # Handle AJAX requests
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': f"Event '{event.title}' added successfully!"
                    })
                
                return redirect("dashboard")
            else:
                messages.error(request, "Please correct the event form errors.")
                print(f"Event form errors: {form.errors}")
                
                # Handle AJAX requests with errors
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Please correct the event form errors.',
                        'errors': dict(form.errors)
                    })
                
                event_form = form # Re-assign the form with errors
        
        # If we get here and it's an AJAX request, something went wrong
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred. Please try again.'
            })

    # Get all necessary data for the dashboard view
    upcoming_assignments = Assignment.objects.filter(
        course__user=request.user,
        due_date__gte=timezone.now(),
        completed=False
    ).order_by("due_date")

    overdue_assignments = Assignment.objects.filter(
        course__user=request.user,
        due_date__lt=timezone.now(),
        completed=False
    ).order_by("due_date")

    upcoming_exams = Exam.objects.filter(
        course__user=request.user,
        exam_date__gte=timezone.now()
    ).order_by("exam_date")

    upcoming_events = CalendarEvent.objects.filter(
        user=request.user,
        event_date__gte=timezone.now()
    ).order_by("event_date")

    context = {
        "courses": user_courses,
        "upcoming_assignments": upcoming_assignments,
        "overdue_assignments": overdue_assignments,
        "upcoming_exams": upcoming_exams,
        "upcoming_events": upcoming_events,
        "course_form": course_form,
        "assignment_form": assignment_form,
        "exam_form": exam_form,
        "event_form": event_form,
    }

    return render(request, "index.html", context)


@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, course__user=request.user)

    if request.method == "POST":
        form = AssignmentEditForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect("dashboard")
    else:
        form = AssignmentEditForm(instance=assignment)

    return render(request, "academic_app/edit_assignment.html", {
        "form": form,
        "assignment": assignment
    })


@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, course__user=request.user)

    if request.method == "POST":
        assignment.delete()
        messages.success(request, "Assignment deleted successfully!")
        return redirect("dashboard")

    return render(request, "academic_app/delete_assignment.html", {
        "assignment": assignment
    })


@login_required
@require_POST
def toggle_assignment_completion(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, course__user=request.user)
    assignment.completed = not assignment.completed
    assignment.save()

    status = "completed" if assignment.completed else "marked as incomplete"
    return JsonResponse({
        "success": True,
        "message": f"Assignment {status}",
        "completed": assignment.completed
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, user=request.user)

    assignments = course.assignments.all().order_by("due_date")
    exams = course.exams.all().order_by("exam_date")
    attendance_records = course.attendance_records.all().order_by("-date")

    # Calculate attendance percentage
    total_classes = attendance_records.count()
    present_classes = attendance_records.filter(present=True).count()
    attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0

    context = {
        "course": course,
        "assignments": assignments,
        "exams": exams,
        "attendance_records": attendance_records,
        "attendance_percentage": round(attendance_percentage, 1),
        "total_classes": total_classes,
        "present_classes": present_classes,
    }

    return render(request, "academic_app/course_detail.html", context)


@login_required
def calendar_data(request):
    """API endpoint to provide calendar data for FullCalendar"""
    user_assignments = Assignment.objects.filter(course__user=request.user)
    user_exams = Exam.objects.filter(course__user=request.user)
    user_events = CalendarEvent.objects.filter(user=request.user)

    events = []

    # Add assignments
    for assignment in user_assignments:
        events.append({
            "id": f"assignment-{assignment.id}",
            "title": f"📝 {assignment.title}",
            "start": assignment.due_date.isoformat(),
            "color": assignment.course.color,
            "extendedProps": {
                "type": "assignment",
                "course": assignment.course.name,
                "priority": assignment.priority,
                "completed": assignment.completed
            }
        })

    # Add exams
    for exam in user_exams:
        events.append({
            "id": f"exam-{exam.id}",
            "title": f"📋 {exam.title}",
            "start": exam.exam_date.isoformat(),
            "color": exam.course.color,
            "extendedProps": {
                "type": "exam",
                "course": exam.course.name,
                "exam_type": exam.exam_type
            }
        })

    # Add events
    for event in user_events:
        events.append({
            "id": f"event-{event.id}",
            "title": f"🎉 {event.title}",
            "start": event.event_date.isoformat(),
            "end": event.end_date.isoformat() if event.end_date else None,
            "color": event.color,
            "extendedProps": {
                "type": "event",
                "event_type": event.event_type,
                "location": event.location
            }
        })

    return JsonResponse(events, safe=False)


@login_required
def debug_forms(request):
    """Debug page for testing form functionality"""
    user_courses = Course.objects.filter(user=request.user)

    context = {
        "courses": user_courses,
    }

    return render(request, "debug_forms.html", context)


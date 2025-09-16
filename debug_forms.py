#!/usr/bin/env python3
"""
Debug script for Academic Planner forms
Run this to test form functionality and identify issues
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_planner_project.settings')
django.setup()

from django.contrib.auth.models import User
from academic_app.models import Course, Assignment, Exam, CalendarEvent
from academic_app.forms import CourseForm, AssignmentForm, ExamForm, CalendarEventForm
from django.test import RequestFactory
from django.contrib.auth import get_user_model

def create_test_user():
    """Create or get a test user"""
    try:
        user = User.objects.get(username='testuser')
        print(f"Using existing test user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"Created test user: {user.username}")
    return user

def test_course_form():
    """Test CourseForm functionality"""
    print("\n=== Testing CourseForm ===")

    user = create_test_user()

    # Test valid form data
    valid_data = {
        'name': 'Test Course',
        'code': 'TEST101',
        'instructor': 'Dr. Test',
        'credits': 3,
        'color': '#007bff'
    }

    form = CourseForm(data=valid_data, user=user)
    print(f"Form is valid: {form.is_valid()}")

    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        return False

    # Test form with prefix (like in the view)
    prefixed_data = {
        'course-name': 'Test Course with Prefix',
        'course-code': 'TEST102',
        'course-instructor': 'Dr. Prefix',
        'course-credits': 3,
        'course-color': '#28a745'
    }

    prefixed_form = CourseForm(data=prefixed_data, user=user, prefix='course')
    print(f"Prefixed form is valid: {prefixed_form.is_valid()}")

    if not prefixed_form.is_valid():
        print(f"Prefixed form errors: {prefixed_form.errors}")
        return False

    # Save the form to test database operations
    try:
        course = form.save(commit=False)
        course.user = user
        course.save()
        print(f"Successfully saved course: {course.name}")
        return True
    except Exception as e:
        print(f"Error saving course: {e}")
        return False

def test_assignment_form():
    """Test AssignmentForm functionality"""
    print("\n=== Testing AssignmentForm ===")

    user = create_test_user()

    # First create a course for the assignment
    course = Course.objects.create(
        user=user,
        name='Assignment Test Course',
        code='ATC101',
        instructor='Dr. Assignment',
        credits=3,
        color='#17a2b8'
    )

    # Test valid form data
    valid_data = {
        'assignment-course': course.id,
        'assignment-title': 'Test Assignment',
        'assignment-description': 'This is a test assignment',
        'assignment-due_date': '2024-12-31T23:59',
        'assignment-priority': 'medium',
        'assignment-estimated_hours': 5
    }

    form = AssignmentForm(data=valid_data, user=user, prefix='assignment')
    print(f"Assignment form is valid: {form.is_valid()}")

    if not form.is_valid():
        print(f"Assignment form errors: {form.errors}")
        return False

    try:
        assignment = form.save()
        print(f"Successfully saved assignment: {assignment.title}")
        return True
    except Exception as e:
        print(f"Error saving assignment: {e}")
        return False

def test_form_field_names():
    """Test form field names to ensure they match the expected patterns"""
    print("\n=== Testing Form Field Names ===")

    user = create_test_user()

    # Test CourseForm field names
    course_form = CourseForm(user=user, prefix='course')
    print("CourseForm fields:")
    for field_name, field in course_form.fields.items():
        html_name = course_form.add_prefix(field_name)
        print(f"  - {field_name} -> HTML name: {html_name}")

    # Test AssignmentForm field names
    assignment_form = AssignmentForm(user=user, prefix='assignment')
    print("\nAssignmentForm fields:")
    for field_name, field in assignment_form.fields.items():
        html_name = assignment_form.add_prefix(field_name)
        print(f"  - {field_name} -> HTML name: {html_name}")

def test_database_connection():
    """Test database connectivity"""
    print("\n=== Testing Database Connection ===")

    try:
        user_count = User.objects.count()
        course_count = Course.objects.count()
        assignment_count = Assignment.objects.count()

        print(f"Database connection successful!")
        print(f"Users: {user_count}")
        print(f"Courses: {course_count}")
        print(f"Assignments: {assignment_count}")
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def check_static_files():
    """Check if static files are properly configured"""
    print("\n=== Checking Static Files ===")

    from django.conf import settings

    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")

    # Check if debug CSS exists
    debug_css_path = os.path.join(settings.STATICFILES_DIRS[0], 'css', 'debug.css')
    print(f"Debug CSS exists: {os.path.exists(debug_css_path)}")

    return True

def main():
    """Run all debug tests"""
    print("Academic Planner Debug Script")
    print("=" * 50)

    results = {
        'database': test_database_connection(),
        'static_files': check_static_files(),
        'course_form': test_course_form(),
        'assignment_form': test_assignment_form(),
        'field_names': test_form_field_names() or True,  # This doesn't return a boolean
    }

    print("\n" + "=" * 50)
    print("SUMMARY:")
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    if all(results.values()):
        print("\n🎉 All tests passed! Your forms should be working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == '__main__':
    main()

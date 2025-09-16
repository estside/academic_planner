#!/usr/bin/env python3
"""
Simple form test script to check if forms are working correctly
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_planner_project.settings')
django.setup()

from django.contrib.auth.models import User
from academic_app.forms import CourseForm, AssignmentForm, ExamForm, CalendarEventForm

def test_form_rendering():
    """Test if forms render correctly with prefixes"""
    print("=== Testing Form Rendering ===")

    # Create test user
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user('testuser', 'test@test.com', 'testpass')

    # Test forms with prefixes (as used in views)
    course_form = CourseForm(user=user, prefix='course')
    assignment_form = AssignmentForm(user=user, prefix='assignment')
    exam_form = ExamForm(user=user, prefix='exam')
    event_form = CalendarEventForm(prefix='event')

    print("Course form fields:")
    for field_name in course_form.fields:
        html_name = course_form.add_prefix(field_name)
        print(f"  {field_name} -> {html_name}")

    print("\nAssignment form fields:")
    for field_name in assignment_form.fields:
        html_name = assignment_form.add_prefix(field_name)
        print(f"  {field_name} -> {html_name}")

    print("\nForms created successfully!")
    return True

def test_form_data():
    """Test form submission with proper prefixed data"""
    print("\n=== Testing Form Submission Data ===")

    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user('testuser', 'test@test.com', 'testpass')

    # Test data with prefixes (as would come from browser)
    course_data = {
        'course-name': 'Test Course',
        'course-code': 'TEST123',
        'course-instructor': 'Dr. Test',
        'course-credits': 3,
        'course-color': '#007bff'
    }

    course_form = CourseForm(data=course_data, user=user, prefix='course')

    print(f"Course form valid: {course_form.is_valid()}")
    if not course_form.is_valid():
        print(f"Course form errors: {course_form.errors}")
        return False

    print("Form validation successful!")
    return True

if __name__ == '__main__':
    success = True
    success &= test_form_rendering()
    success &= test_form_data()

    if success:
        print("\n✅ All tests passed! Forms should be working correctly.")
    else:
        print("\n❌ Some tests failed.")

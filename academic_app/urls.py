from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    
    # Django's built-in login and logout views
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path("assignment/<int:assignment_id>/edit/", views.edit_assignment, name="edit_assignment"),
    path("assignment/<int:assignment_id>/delete/", views.delete_assignment, name="delete_assignment"),
    path("assignment/<int:assignment_id>/toggle/", views.toggle_assignment_completion, name="toggle_assignment"),
    path("calendar-data/", views.calendar_data, name="calendar_data"),
    path("debug-forms/", views.debug_forms, name="debug_forms"),
]
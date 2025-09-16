from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Course, Assignment, Exam, Attendance, CalendarEvent


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'instructor', 'credits', 'user', 'created_at', 'color_display']
    list_filter = ['user', 'credits', 'created_at']
    search_fields = ['name', 'code', 'instructor']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'code', 'instructor')
        }),
        ('Details', {
            'fields': ('credits', 'color_display', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        if obj.color:
            return format_html(
                '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></span> {}',
                obj.color, obj.color
            )
        return '-'
    color_display.short_description = 'Color'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'priority', 'completed', 'user', 'is_overdue_display']
    list_filter = ['completed', 'priority', 'course__user', 'due_date']
    search_fields = ['title', 'course__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'is_overdue_display']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('course', 'title', 'description')
        }),
        ('Timing & Priority', {
            'fields': ('due_date', 'priority', 'estimated_hours', 'completed')
        }),
        ('Status', {
            'fields': ('is_overdue_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user(self, obj):
        return obj.course.user.username
    user.short_description = 'User'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ OVERDUE</span>')
        return format_html('<span style="color: green;">✅ On Time</span>')
    is_overdue_display.short_description = 'Status'


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'exam_type', 'exam_date', 'duration', 'location', 'user']
    list_filter = ['exam_type', 'course__user', 'exam_date']
    search_fields = ['title', 'course__name', 'location', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'exam_date'
    
    fieldsets = (
        ('Exam Details', {
            'fields': ('course', 'title', 'exam_type')
        }),
        ('Schedule & Location', {
            'fields': ('exam_date', 'duration', 'location')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user(self, obj):
        return obj.course.user.username
    user.short_description = 'User'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['course', 'date', 'present', 'user', 'created_at']
    list_filter = ['present', 'course__user', 'date']
    search_fields = ['course__name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Record', {
            'fields': ('course', 'date', 'present')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user(self, obj):
        return obj.course.user.username
    user.short_description = 'User'


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'end_date', 'location', 'user', 'color_display']
    list_filter = ['event_type', 'user', 'event_date']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('user', 'title', 'event_type')
        }),
        ('Schedule & Location', {
            'fields': ('event_date', 'end_date', 'location')
        }),
        ('Description & Styling', {
            'fields': ('description', 'color_display', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        if obj.color:
            return format_html(
                '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></span> {}',
                obj.color, obj.color
            )
        return '-'
    color_display.short_description = 'Color'


# Customize admin site
admin.site.site_header = "Academic Planner Administration"
admin.site.site_title = "Academic Planner Admin"
admin.site.index_title = "Welcome to Academic Planner Administration"

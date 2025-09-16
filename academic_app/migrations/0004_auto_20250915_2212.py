# Generated manually to handle model updates

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('academic_app', '0003_remove_assignment_completed_and_more'),
    ]

    operations = [
        # Remove duplicate Attendance model
        migrations.DeleteModel(
            name='Attendance',
        ),
        
        # Update Course model
        migrations.RenameField(
            model_name='course',
            old_name='user',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(help_text="Course name (e.g., 'Advanced Mathematics')", max_length=200, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AddField(
            model_name='course',
            name='credits',
            field=models.PositiveIntegerField(default=3, help_text='Number of credit hours'),
        ),
        migrations.AddField(
            model_name='course',
            name='color',
            field=models.CharField(default='#007bff', help_text='Color for calendar display (hex code)', max_length=7),
        ),
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['name']},
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('user', 'code'), name='unique_user_course_code'),
        ),
        
        # Update Assignment model
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, help_text='Assignment description or instructions', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium', help_text='Priority level', max_length=10),
        ),
        migrations.AddField(
            model_name='assignment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assignment',
            name='estimated_hours',
            field=models.PositiveIntegerField(default=1, help_text='Estimated time to complete (hours)'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(help_text='Assignment title', max_length=200, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['due_date', 'priority']},
        ),
        
        # Update Exam model
        migrations.AddField(
            model_name='exam',
            name='exam_type',
            field=models.CharField(choices=[('midterm', 'Midterm'), ('final', 'Final'), ('quiz', 'Quiz'), ('project', 'Project'), ('presentation', 'Presentation')], default='midterm', help_text='Type of exam', max_length=20),
        ),
        migrations.AddField(
            model_name='exam',
            name='duration',
            field=models.PositiveIntegerField(default=120, help_text='Duration in minutes'),
        ),
        migrations.AddField(
            model_name='exam',
            name='location',
            field=models.CharField(blank=True, help_text='Exam location', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='notes',
            field=models.TextField(blank=True, help_text='Additional notes or topics to study', null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(help_text='Exam title', max_length=200, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['exam_date']},
        ),
        
        # Update CalendarEvent model
        migrations.AddField(
            model_name='calendarevent',
            name='end_date',
            field=models.DateTimeField(blank=True, help_text='Event end time (optional)', null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='event_type',
            field=models.CharField(choices=[('personal', 'Personal'), ('academic', 'Academic'), ('social', 'Social'), ('other', 'Other')], default='personal', help_text='Type of event', max_length=20),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='location',
            field=models.CharField(blank=True, help_text='Event location', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='color',
            field=models.CharField(default='#28a745', help_text='Color for calendar display (hex code)', max_length=7),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='title',
            field=models.CharField(help_text='Event title', max_length=200, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterModelOptions(
            name='calendarevent',
            options={'ordering': ['event_date']},
        ),
        
        # Create new Attendance model
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Class date')),
                ('present', models.BooleanField(default=True, help_text='Present or absent')),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the class', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='academic_app.course')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('course', 'date'), name='unique_course_date'),
        ),
    ]
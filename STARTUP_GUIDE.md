# Academic Planner Startup Guide

## Quick Start Instructions

### 1. Navigate to Project Directory
```bash
cd academic_planner_project
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Apply Database Migrations
```bash
python3 manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python3 manage.py createsuperuser
```

### 5. Collect Static Files
```bash
python3 manage.py collectstatic --noinput
```

### 6. Start Development Server
```bash
python3 manage.py runserver
```

### 7. Access the Application
Open your browser and go to: http://127.0.0.1:8000

## Fixed Issues

### ✅ Course Form Submission Issue
- **Problem**: Course form was refreshing instead of submitting
- **Fix**: Added proper user parameter handling in CourseForm POST processing
- **Location**: `academic_app/views.py` line 78

### ✅ FullCalendar Loading Errors
- **Problem**: 404 errors for main.min.css and main.min.js files
- **Fix**: Updated CDN links to use FullCalendar v6.1.15 with proper URLs
- **Location**: `templates/index.html` line 7

### ✅ Static Files Configuration
- **Problem**: Missing static files causing 404 errors
- **Fix**: Added debug CSS and proper static file handling
- **Location**: `static/css/debug.css` and updated `templates/base.html`

### ✅ Form Validation
- **Problem**: Forms not providing proper feedback on validation errors
- **Fix**: Added client-side validation with visual feedback
- **Location**: `templates/index.html` JavaScript section

## Troubleshooting

### Form Still Not Submitting?

1. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Verify FullCalendar is loaded

2. **Check Django Logs**
   ```bash
   # In your terminal where you ran runserver
   # Look for error messages
   ```

3. **Verify Form Fields**
   - Make sure all required fields are filled
   - Check that course name and code are not empty

### FullCalendar Not Loading?

1. **Check Internet Connection**
   - FullCalendar loads from CDN
   - Verify you can access: https://cdn.jsdelivr.net/npm/fullcalendar@6.1.15/

2. **Fallback Display**
   - If FullCalendar fails, you'll see a fallback message
   - Click "Refresh" to try again

3. **Browser Cache**
   ```bash
   # Clear browser cache or try incognito mode
   ```

### Database Issues?

1. **Reset Database**
   ```bash
   rm db.sqlite3
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

2. **Check Migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

## Testing Form Functionality

Run the debug script to test all forms:
```bash
python3 debug_forms.py
```

This will test:
- Database connectivity
- Course form submission
- Assignment form submission
- Static files configuration
- Form field name mappings

## Key Features Working

### ✅ Course Management
- Add new courses with name, code, instructor, credits, and color
- View course list in dashboard
- Course-specific detail pages

### ✅ Assignment Tracking
- Add assignments with due dates and priorities
- Mark assignments as complete/incomplete
- Visual priority indicators
- Overdue assignment warnings

### ✅ Calendar Integration
- FullCalendar displays all assignments, exams, and events
- Click events for detailed information
- Month and list view options

### ✅ Form Validation
- Client-side validation with visual feedback
- Server-side validation with error messages
- Loading states during form submission

## Development Tips

### Debug Mode
The application includes debug features when running on localhost:
- Debug information appears in top-right corner
- Console logging for JavaScript events
- Visual form validation feedback

### Adding New Features
1. Update models in `academic_app/models.py`
2. Create/update forms in `academic_app/forms.py`
3. Add views in `academic_app/views.py`
4. Update templates in `templates/`
5. Add URL patterns in `academic_app/urls.py`

### Static Files
- CSS files go in `static/css/`
- JavaScript files go in `static/js/`
- Images go in `static/images/`
- Run `python3 manage.py collectstatic` after adding new files

## Support

If you encounter issues:

1. **Check this guide first**
2. **Run the debug script**: `python3 debug_forms.py`
3. **Check browser console** for JavaScript errors
4. **Check Django logs** in the terminal
5. **Verify all requirements** are installed

## Recent Changes

- Updated FullCalendar CDN links to v6.1.15
- Fixed CourseForm user parameter handling
- Added comprehensive form validation
- Improved error handling and user feedback
- Added debug CSS and utilities
- Enhanced static file management

The application should now work correctly for course submission and all other features!
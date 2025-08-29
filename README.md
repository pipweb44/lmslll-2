# EduPlatform - Learning Management System

A comprehensive Learning Management System (LMS) built with Django, similar to Coursera, featuring student enrollment workflows, teacher course management, and admin approval systems.

## Features

### 🎓 Student Features
- **Course Browsing**: Search and filter courses by category, difficulty, and keywords
- **Enrollment System**: Submit enrollment requests with contact information
- **Progress Tracking**: Track course completion and video progress
- **Course Reviews**: Rate and review completed courses
- **Personal Dashboard**: View enrolled courses and enrollment request status

### 👨‍🏫 Teacher Features
- **Course Management**: Create, edit, and delete courses
- **Content Management**: Add modules, videos, and assignments
- **Student Analytics**: View enrolled students and course statistics
- **Teacher Dashboard**: Comprehensive overview of all courses and metrics

### 🔧 Admin Features
- **Enrollment Approval**: Review and approve/reject student enrollment requests
- **User Management**: Manage student and teacher accounts
- **Content Moderation**: Oversee all courses and content
- **System Analytics**: Monitor platform usage and performance

## System Architecture

### Apps Structure
- **accounts**: User management, profiles, authentication
- **courses**: Course content, modules, videos, categories
- **enrollments**: Enrollment requests, approvals, progress tracking
- **ratings**: Course ratings and reviews system

### Key Models
- **User**: Custom user model with role-based access (Student/Teacher/Admin)
- **Course**: Course information with instructor, category, pricing
- **EnrollmentRequest**: Student enrollment requests with admin approval workflow
- **Enrollment**: Approved enrollments with progress tracking
- **Rating**: Course ratings and reviews system

## Installation & Setup

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create Sample Data**:
   ```bash
   python manage.py setup_sample_data
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

## Default Login Credentials

- **Admin**: `admin` / `admin123`
- **Teacher**: `teacher1` / `password123`
- **Student**: `student1` / `password123`

## Usage Workflow

### For Students:
1. Register as a student
2. Browse available courses
3. Submit enrollment request with contact information
4. Wait for admin approval
5. Once approved, access course content and track progress
6. Rate and review completed courses

### For Teachers:
1. Register as a teacher
2. Access teacher dashboard
3. Create and manage courses
4. Add modules and videos to courses
5. Monitor student enrollments and progress

### For Admins:
1. Access Django admin panel at `/admin/`
2. Review enrollment requests
3. Approve/reject requests with bulk actions
4. Manage users, courses, and system content

## Key Features Implemented

✅ **User Authentication & Roles**
✅ **Course Management System**
✅ **Enrollment Request Workflow**
✅ **Admin Approval System**
✅ **Progress Tracking**
✅ **Rating & Review System**
✅ **Responsive Coursera-like UI**
✅ **Teacher & Student Dashboards**
✅ **Video Content Management**

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5.3, Font Awesome, Google Fonts
- **Media Handling**: Django file uploads
- **Authentication**: Django's built-in auth system

## File Structure

```
lmslll/
├── accounts/          # User management
├── courses/           # Course content
├── enrollments/       # Enrollment system
├── ratings/           # Rating system
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # Uploaded files
└── core/             # Django settings
```

The system is now fully functional and ready for use!

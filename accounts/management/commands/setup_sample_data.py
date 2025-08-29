from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course
from accounts.models import StudentProfile, TeacherProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the LMS system'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Programming', 'description': 'Learn programming languages and software development'},
            {'name': 'Data Science', 'description': 'Master data analysis and machine learning'},
            {'name': 'Design', 'description': 'UI/UX design and graphic design courses'},
            {'name': 'Business', 'description': 'Business and entrepreneurship skills'},
            {'name': 'Marketing', 'description': 'Digital marketing and social media'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample teacher
        teacher, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher@example.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'user_type': 'teacher',
                'phone': '+1234567890'
            }
        )
        if created:
            teacher.set_password('password123')
            teacher.save()
            TeacherProfile.objects.create(
                user=teacher,
                specialization='Web Development',
                experience_years=5,
                qualifications='MSc Computer Science',
                is_verified=True
            )
            self.stdout.write(f'Created teacher: {teacher.username}')
        
        # Create sample student
        student, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student@example.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'user_type': 'student',
                'phone': '+1234567891'
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            StudentProfile.objects.create(
                user=student,
                student_id='STU000001',
                education_level='Bachelor Degree',
                interests='Web Development, AI'
            )
            self.stdout.write(f'Created student: {student.username}')
        
        # Create sample courses
        programming_cat = Category.objects.get(name='Programming')
        
        courses_data = [
            {
                'title': 'Complete Python Programming Bootcamp',
                'short_description': 'Learn Python from beginner to advanced level',
                'description': 'Master Python programming with hands-on projects and real-world applications.',
                'category': programming_cat,
                'price': 99.99,
                'difficulty': 'beginner',
                'duration_weeks': 8,
                'is_published': True
            },
            {
                'title': 'Web Development with Django',
                'short_description': 'Build web applications using Django framework',
                'description': 'Create powerful web applications using Django, the Python web framework.',
                'category': programming_cat,
                'price': 149.99,
                'difficulty': 'intermediate',
                'duration_weeks': 10,
                'is_published': True
            }
        ]
        
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    **course_data,
                    'instructor': teacher
                }
            )
            if created:
                self.stdout.write(f'Created course: {course.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Teacher: teacher1 / password123')
        self.stdout.write('Student: student1 / password123')

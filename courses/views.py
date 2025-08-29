from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Course, Category, Module, Video
from .forms import CourseForm, ModuleForm, VideoForm
from enrollments.models import Enrollment

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.models import User
        
        # Featured courses (top 6 by rating)
        context['featured_courses'] = Course.objects.filter(is_published=True).select_related('instructor', 'category').annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')[:6]
        
        # Categories
        context['categories'] = Category.objects.all()[:8]
        
        # Stats
        context['total_courses'] = Course.objects.filter(is_published=True).count()
        context['total_students'] = User.objects.filter(user_type='student').count()
        context['total_teachers'] = User.objects.filter(user_type='teacher').count()
        context['total_hours'] = sum(course.modules.all().count() * 2 for course in Course.objects.filter(is_published=True)) or 100  # Estimate 2 hours per module
        
        return context

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True).select_related('instructor', 'category')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(instructor__username__icontains=search)
            )
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
            
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        return queryset.annotate(avg_rating=Avg('ratings__score'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['difficulties'] = Course.DIFFICULTY_CHOICES
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        if self.request.user.is_authenticated:
            context['user_enrolled'] = Enrollment.objects.filter(
                student=self.request.user, 
                course=course,
                enrollment_request__status='approved'
            ).exists()
            context['enrollment_request'] = course.enrollment_requests.filter(
                student=self.request.user
            ).first()
        
        context['modules'] = course.modules.prefetch_related('videos')
        context['ratings'] = course.ratings.select_related('student')[:5]
        context['avg_rating'] = course.average_rating
        return context

class CoursesByCategoryView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Course.objects.filter(
            category_id=category_id, 
            is_published=True
        ).select_related('instructor', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        return context

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/teacher_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'Access denied. Teacher account required.')
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        courses = user.courses_taught.all()
        
        context['courses'] = courses
        context['total_courses'] = courses.count()
        context['total_students'] = sum(course.total_students for course in courses)
        context['pending_requests'] = sum(
            course.enrollment_requests.filter(status='pending').count() 
            for course in courses
        )
        return context

class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'Access denied. Teacher account required.')
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class EditCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/edit_course.html'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)

class DeleteCourseView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy('courses:teacher_dashboard')
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

class ManageModulesView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/manage_modules.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(
            Course, 
            slug=self.kwargs['slug'], 
            instructor=self.request.user
        )
        context['course'] = course
        context['modules'] = course.modules.prefetch_related('videos')
        return context

class VideoPlayerView(LoginRequiredMixin, DetailView):
    model = Video
    template_name = 'courses/video_player.html'
    context_object_name = 'video'
    pk_url_kwarg = 'video_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        course = video.module.course
        
        # Check if user is enrolled
        enrollment = Enrollment.objects.filter(
            student=self.request.user,
            course=course,
            enrollment_request__status='approved'
        ).first()
        
        if not enrollment and not video.is_free:
            messages.error(self.request, 'You need to be enrolled to watch this video.')
            return redirect('courses:course_detail', slug=course.slug)
        
        # Get all videos in course order
        all_videos = Video.objects.filter(module__course=course).order_by('module__order', 'order')
        video_list = list(all_videos)
        
        try:
            current_index = video_list.index(video)
            context['previous_video'] = video_list[current_index - 1] if current_index > 0 else None
            context['next_video'] = video_list[current_index + 1] if current_index < len(video_list) - 1 else None
        except ValueError:
            context['previous_video'] = None
            context['next_video'] = None
        
        context['course'] = course
        context['enrollment'] = enrollment
        context['user_enrolled'] = bool(enrollment)
        return context

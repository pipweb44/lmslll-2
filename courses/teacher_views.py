from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Course, Category, Module, Video, Post
from .forms import CourseForm, ModuleForm, VideoForm, PostForm
from enrollments.models import Enrollment, VideoProgress

# Comprehensive Course Management Views
class CourseManagementView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_management.html'
    context_object_name = 'course'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'Access denied. Teachers only.')
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        
        # Students and progress
        enrollments = course.enrollments.select_related('student').all()
        context['enrollments'] = enrollments
        context['total_students'] = enrollments.count()
        
        # Modules and videos
        modules = course.modules.prefetch_related('videos').all()
        context['modules'] = modules
        context['total_modules'] = modules.count()
        context['total_videos'] = Video.objects.filter(module__course=course).count()
        
        # Posts
        context['posts'] = course.posts.all()[:5]
        context['total_posts'] = course.posts.count()
        
        # Statistics
        context['avg_progress'] = enrollments.aggregate(
            avg_progress=Avg('progress_percentage')
        )['avg_progress'] or 0
        
        return context

class StudentProgressView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/student_progress.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        
        # Detailed student progress
        enrollments = course.enrollments.select_related('student').prefetch_related(
            'video_progress__video'
        ).all()
        
        student_progress = []
        for enrollment in enrollments:
            videos_watched = enrollment.video_progress.filter(is_completed=True).count()
            total_videos = Video.objects.filter(module__course=course).count()
            
            student_progress.append({
                'enrollment': enrollment,
                'videos_watched': videos_watched,
                'total_videos': total_videos,
                'completion_rate': (videos_watched / total_videos * 100) if total_videos > 0 else 0,
                'last_activity': enrollment.video_progress.order_by('-last_watched').first()
            })
        
        context['student_progress'] = student_progress
        return context

# Post Management Views
class CoursePostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'courses/course_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(
            Course, 
            slug=self.kwargs['slug'], 
            instructor=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Post.objects.filter(course=self.course)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'courses/create_post.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(
            Course, 
            slug=self.kwargs['slug'], 
            instructor=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.course = self.course
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_posts', kwargs={'slug': self.course.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'courses/edit_post.html'
    
    def get_queryset(self):
        return Post.objects.filter(
            course__instructor=self.request.user,
            course__slug=self.kwargs['slug']
        )
    
    def get_success_url(self):
        return reverse_lazy('courses:course_posts', kwargs={'slug': self.object.course.slug})

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'courses/delete_post.html'
    
    def get_queryset(self):
        return Post.objects.filter(course__instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_posts', kwargs={'slug': self.object.course.slug})

# Enhanced Module and Video Management
class CreateModuleView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/create_module.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(
            Course, 
            slug=self.kwargs['slug'], 
            instructor=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.course = self.course
        messages.success(self.request, 'Module created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.course.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

class CreateVideoView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'courses/create_video.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.module = get_object_or_404(
            Module, 
            id=self.kwargs['module_id'],
            course__instructor=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.module = self.module
        messages.success(self.request, 'Video added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.module.course.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        context['course'] = self.module.course
        return context

class EditModuleView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/edit_module.html'
    
    def get_queryset(self):
        return Module.objects.filter(course__instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.object.course.slug})

class DeleteModuleView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = 'courses/delete_module.html'
    
    def get_queryset(self):
        return Module.objects.filter(course__instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.object.course.slug})

class EditVideoView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'courses/edit_video.html'
    
    def get_queryset(self):
        return Video.objects.filter(module__course__instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.object.module.course.slug})

class DeleteVideoView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'courses/delete_video.html'
    
    def get_queryset(self):
        return Video.objects.filter(module__course__instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:manage_modules', kwargs={'slug': self.object.module.course.slug})

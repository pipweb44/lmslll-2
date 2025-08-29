from django.urls import path
from . import views
from . import teacher_views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('category/<int:category_id>/', views.CoursesByCategoryView.as_view(), name='courses_by_category'),
    path('teacher/dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher/course/create/', views.CreateCourseView.as_view(), name='create_course'),
    path('teacher/course/<slug:slug>/edit/', views.EditCourseView.as_view(), name='edit_course'),
    path('teacher/course/<slug:slug>/delete/', views.DeleteCourseView.as_view(), name='delete_course'),
    path('teacher/course/<slug:slug>/modules/', views.ManageModulesView.as_view(), name='manage_modules'),
    path('course/<slug:slug>/watch/<int:video_id>/', views.VideoPlayerView.as_view(), name='video_player'),
    
    # Comprehensive Teacher Management URLs
    path('teacher/course/<slug:slug>/manage/', teacher_views.CourseManagementView.as_view(), name='course_management'),
    path('teacher/course/<slug:slug>/students/', teacher_views.StudentProgressView.as_view(), name='student_progress'),
    
    # Posts Management
    path('teacher/course/<slug:slug>/posts/', teacher_views.CoursePostsView.as_view(), name='course_posts'),
    path('teacher/course/<slug:slug>/posts/create/', teacher_views.CreatePostView.as_view(), name='create_post'),
    path('teacher/course/<slug:slug>/posts/<int:pk>/edit/', teacher_views.EditPostView.as_view(), name='edit_post'),
    path('teacher/posts/<int:pk>/delete/', teacher_views.DeletePostView.as_view(), name='delete_post'),
    
    # Module Management
    path('teacher/course/<slug:slug>/modules/create/', teacher_views.CreateModuleView.as_view(), name='create_module'),
    path('teacher/modules/<int:pk>/edit/', teacher_views.EditModuleView.as_view(), name='edit_module'),
    path('teacher/modules/<int:pk>/delete/', teacher_views.DeleteModuleView.as_view(), name='delete_module'),
    
    # Video Management
    path('teacher/module/<int:module_id>/videos/create/', teacher_views.CreateVideoView.as_view(), name='create_video'),
    path('teacher/videos/<int:pk>/edit/', teacher_views.EditVideoView.as_view(), name='edit_video'),
    path('teacher/videos/<int:pk>/delete/', teacher_views.DeleteVideoView.as_view(), name='delete_video'),
]

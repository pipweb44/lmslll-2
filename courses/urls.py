from django.urls import path
from . import views

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
]

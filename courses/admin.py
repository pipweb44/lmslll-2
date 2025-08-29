from django.contrib import admin
from .models import Category, Course, Module, Video, Assignment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'price', 'is_published', 'created_at']
    list_filter = ['category', 'difficulty', 'is_published', 'created_at']
    search_fields = ['title', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    inlines = [VideoInline]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'duration_minutes', 'is_free', 'order']
    list_filter = ['is_free', 'module__course']
    search_fields = ['title', 'module__title']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'due_date', 'max_score']
    list_filter = ['module__course', 'due_date']
    search_fields = ['title', 'module__title']

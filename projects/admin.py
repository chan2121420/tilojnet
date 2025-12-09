from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'service_category', 'order', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    list_filter = ['service_category']
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'location', 'is_featured', 'is_published', 'views_count', 'image_preview']
    list_filter = ['category', 'service_categories', 'status', 'is_featured', 'is_published', 'project_date']
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title', 'client_name', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'project_date'
    inlines = [ProjectImageInline]
    filter_horizontal = ['service_categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'service_categories', 'status')
        }),
        ('Project Details', {
            'fields': ('client_name', 'location', 'project_date', 'budget_range', 'duration', 'area_sqm')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'challenge', 'solution', 'result', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Options', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" />', obj.featured_image.url)
        return '-'
    image_preview.short_description = 'Preview'

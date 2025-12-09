from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_featured', 'item_count', 'image_preview']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_featured']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Images', {
            'fields': ('featured_image', 'banner_image')
        }),
        ('Options', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def item_count(self, obj):
        count = obj.items.count()
        return format_html('<span class="badge badge-info">{}</span>', count)
    item_count.short_description = 'Items'
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" />', obj.featured_image.url)
        return '-'
    image_preview.short_description = 'Preview'


class CategoryItemImageInline(admin.TabularInline):
    model = CategoryItemImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(CategoryItem)
class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_range', 'duration', 'is_popular', 'is_new', 'order', 'image_preview']
    list_filter = ['category', 'is_popular', 'is_new', 'created_at']
    list_editable = ['is_popular', 'is_new', 'order']
    search_fields = ['name', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    inlines = [CategoryItemImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description')
        }),
        ('Images', {
            'fields': ('featured_image',)
        }),
        ('Specifications', {
            'fields': ('price_range', 'duration', 'ideal_space_size')
        }),
        ('Details', {
            'fields': ('key_features', 'materials_used', 'design_styles'),
            'description': 'Enter as JSON arrays, e.g., ["Feature 1", "Feature 2"]'
        }),
        ('Options', {
            'fields': ('is_popular', 'is_new', 'order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" />', obj.featured_image.url)
        return '-'
    image_preview.short_description = 'Preview'


from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, QuoteRequest, Newsletter


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_category', 'location', 'budget', 'status', 'created_at']
    list_filter = ['service_category', 'budget', 'status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'location', 'project_description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    filter_horizontal = ['category_items']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Project Details', {
            'fields': ('service_category', 'category_items', 'location', 'budget', 'timeline', 'project_description')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
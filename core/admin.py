from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import *

class TilojnetAdminSite(admin.AdminSite):
    site_header = mark_safe('<span style="font-size: 24px; font-weight: bold;">🏠 Tilojnet Exclusive</span>')
    site_title = "Tilojnet Admin"
    index_title = mark_safe('<span style="font-size: 20px;">Interior Design Management Dashboard</span>')
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'categories': ServiceCategory.objects.count(),
            'items': CategoryItem.objects.count(),
            'projects': Project.objects.filter(is_published=True).count(),
            'testimonials': Testimonial.objects.count(),
            'pending_contacts': ContactMessage.objects.filter(status='new').count(),
            'pending_quotes': QuoteRequest.objects.filter(status='pending').count(),
            'newsletter_subscribers': Newsletter.objects.filter(is_active=True).count(),
        }
        extra_context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        extra_context['recent_contacts'] = ContactMessage.objects.order_by('-created_at')[:5]
        extra_context['recent_quotes'] = QuoteRequest.objects.order_by('-created_at')[:5]
        extra_context['popular_items'] = CategoryItem.objects.filter(is_popular=True)[:5]
        return super().index(request, extra_context)

admin_site = TilojnetAdminSite(name='tilojnet_admin')

@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'email', 'phone', 'logo_preview']
    fieldsets = (
        ('🏢 Basic Information', {'fields': ('site_name', 'tagline', 'logo', 'favicon')}),
        ('📞 Contact Information', {'fields': ('phone', 'email', 'address', 'whatsapp_number')}),
        ('📝 About Content', {'fields': ('about_short', 'about_full', 'mission', 'vision'), 'classes': ('collapse',)}),
        ('🌐 Social Media', {'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url'), 'classes': ('collapse',)}),
        ('🔍 SEO', {'fields': ('meta_description',), 'classes': ('collapse',)}),
    )
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: contain; border-radius: 10px; border: 2px solid #ddd; padding: 5px;"/>', obj.logo.url)
        return format_html('<span style="color: #999;">No logo</span>')
    logo_preview.short_description = '🖼️ Logo'

@admin.register(HeroSlide, site=admin_site)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('📝 Content', {'fields': ('title', 'subtitle', 'image')}),
        ('🔗 Call to Action', {'fields': ('cta_text', 'cta_link')}),
        ('⚙️ Settings', {'fields': ('order', 'is_active')}),
    )
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 150px; height: 80px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"/>', obj.image.url)
        return '❌'
    image_preview.short_description = '🖼️ Preview'

@admin.register(Testimonial, site=admin_site)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating_stars', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    search_fields = ['client_name', 'client_company', 'testimonial_text']
    date_hierarchy = 'created_at'
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="font-size: 18px;">{}</span>', stars)
    rating_stars.short_description = '⭐ Rating'

@admin.register(TeamMember, site=admin_site)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'years_experience', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'position', 'specialization']

@admin.register(ServiceCategory, site=admin_site)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_display', 'order', 'is_featured', 'item_count', 'image_preview']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_featured']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('📝 Basic Information', {'fields': ('name', 'slug', 'description', 'icon')}),
        ('🖼️ Images', {'fields': ('featured_image', 'banner_image')}),
        ('⚙️ Options', {'fields': ('is_featured', 'order')}),
    )
    def icon_display(self, obj):
        return format_html('<div style="text-align: center; background: #F3F4F6; padding: 10px; border-radius: 8px;"><i class="fas {} fa-2x" style="color: #D97706;"></i></div>', obj.icon)
    icon_display.short_description = '🎨 Icon'
    def item_count(self, obj):
        count = obj.items.count()
        color = '#10B981' if count > 0 else '#EF4444'
        return format_html('<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{}</span>', color, count)
    item_count.short_description = '📊 Items'
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px;"/>', obj.featured_image.url)
        return '-'
    image_preview.short_description = '🖼️'

class CategoryItemImageInline(admin.TabularInline):
    model = CategoryItemImage
    extra = 3
    fields = ['image', 'caption', 'order']

@admin.register(CategoryItem, site=admin_site)
class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_range', 'is_popular', 'is_new', 'order', 'image_preview']
    list_filter = ['category', 'is_popular', 'is_new', 'created_at']
    list_editable = ['order']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    inlines = [CategoryItemImageInline]
    fieldsets = (
        ('📝 Basic Information', {'fields': ('category', 'name', 'slug')}),
        ('📄 Content', {'fields': ('short_description', 'full_description')}),
        ('🖼️ Images', {'fields': ('featured_image',)}),
        ('💰 Specifications', {'fields': ('price_range', 'duration', 'ideal_space_size')}),
        ('✨ Details', {'fields': ('key_features', 'materials_used', 'design_styles')}),
        ('🏷️ Options', {'fields': ('is_popular', 'is_new', 'order')}),
    )
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px;"/>', obj.featured_image.url)
        return '-'
    image_preview.short_description = '🖼️'

@admin.register(ProjectCategory, site=admin_site)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_category', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 5
    fields = ['image', 'caption', 'order']

@admin.register(Project, site=admin_site)
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
        ('📝 Basic Information', {'fields': ('title', 'slug', 'category', 'service_categories', 'status')}),
        ('📋 Project Details', {'fields': ('client_name', 'location', 'project_date', 'budget_range', 'duration', 'area_sqm')}),
        ('📄 Content', {'fields': ('short_description', 'full_description', 'challenge', 'solution', 'result', 'tags')}),
        ('🖼️ Media', {'fields': ('featured_image',)}),
        ('⚙️ Options', {'fields': ('is_featured', 'is_published')}),
    )
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="width: 100px; height: 70px; object-fit: cover; border-radius: 8px;"/>', obj.featured_image.url)
        return '-'
    image_preview.short_description = '🖼️'

@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(QuoteRequest, site=admin_site)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_category', 'location', 'budget', 'status', 'created_at']
    list_filter = ['service_category', 'budget', 'status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'location', 'project_description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    filter_horizontal = ['category_items']

@admin.register(Newsletter, site=admin_site)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
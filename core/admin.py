from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import SiteSettings, HeroSlide, Testimonial, TeamMember

# Import from other apps
from services.models import ServiceCategory, CategoryItem, CategoryItemImage
from projects.models import Project, ProjectCategory, ProjectImage
from contact.models import ContactMessage, QuoteRequest, Newsletter


@admin.register(SiteSettings)
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


@admin.register(HeroSlide)
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


@admin.register(Testimonial)
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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialization', 'years_experience', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'position', 'specialization']


# Also register models from other apps for convenience
class CategoryItemImageInline(admin.TabularInline):
    model = CategoryItemImage
    extra = 3
    fields = ['image', 'caption', 'order']


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_category', 'location', 'budget', 'status', 'created_at']
    list_filter = ['service_category', 'budget', 'status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'location', 'project_description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    filter_horizontal = ['category_items']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
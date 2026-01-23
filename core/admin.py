from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import SiteSettings, HeroSlide, Testimonial, TeamMember


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
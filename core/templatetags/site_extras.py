from django import template
from django.core.cache import cache
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_site_settings():
    """Get site settings with caching and error handling"""
    try:
        # Try to get from cache first
        site_settings = cache.get('site_settings')
        if site_settings is None:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.first()
            
            # If no settings exist, create default ones
            if not site_settings:
                site_settings = create_default_settings()
            
            # Cache for 5 minutes
            if site_settings:
                cache.set('site_settings', site_settings, 300)
        
        return site_settings
    except (OperationalError, ProgrammingError):
        # Database not ready yet (during migrations)
        return get_fallback_settings()
    except Exception as e:
        # Any other error
        print(f"Error loading site settings: {e}")
        return get_fallback_settings()


@register.simple_tag
def get_nav_categories():
    """Get navigation categories with caching and error handling"""
    try:
        categories = cache.get('nav_categories')
        if categories is None:
            from services.models import ServiceCategory
            categories = list(ServiceCategory.objects.all()[:6])
            cache.set('nav_categories', categories, 300)
        return categories
    except (OperationalError, ProgrammingError):
        # Database not ready yet
        return []
    except Exception as e:
        print(f"Error loading categories: {e}")
        return []


def create_default_settings():
    """Create default site settings if none exist"""
    try:
        from core.models import SiteSettings
        
        settings_obj = SiteSettings.objects.create(
            site_name="Tilojnet Exclusive",
            tagline="Premium Interior Design Services",
            phone="+263 771 234 567",
            email="info@tilojnet.com",
            address="123 Design Street, Harare, Zimbabwe",
            whatsapp_number="263771234567",
            about_short="We are a premium interior design company dedicated to transforming spaces into stunning, functional environments.",
            about_full="<p>At Tilojnet Exclusive, we believe every space tells a story.</p>",
            meta_description="Tilojnet Exclusive offers premium interior design services.",
            mission="To transform ordinary spaces into extraordinary experiences.",
            vision="To be Zimbabwe's leading interior design company."
        )
        return settings_obj
    except Exception as e:
        print(f"Error creating default settings: {e}")
        return get_fallback_settings()


def get_fallback_settings():
    """Return a simple object with fallback values when database is unavailable"""
    class FallbackSettings:
        site_name = "Tilojnet Exclusive"
        tagline = "Premium Interior Design Services"
        phone = "+263 771 234 567"
        email = "info@tilojnet.com"
        address = "123 Design Street, Harare, Zimbabwe"
        whatsapp_number = "263771234567"
        about_short = "We are a premium interior design company dedicated to transforming spaces."
        about_full = "<p>At Tilojnet Exclusive, we believe every space tells a story.</p>"
        meta_description = "Tilojnet Exclusive offers premium interior design services."
        mission = "To transform ordinary spaces into extraordinary experiences."
        vision = "To be Zimbabwe's leading interior design company."
        facebook_url = ""
        instagram_url = ""
        twitter_url = ""
        linkedin_url = ""
        logo = None
        favicon = None
    
    return FallbackSettings()


@register.simple_tag
def get_site_value(key, default=""):
    """
    Get a specific site setting value
    Usage: {% get_site_value 'site_name' 'Default Name' %}
    """
    settings_obj = get_site_settings()
    if settings_obj:
        return getattr(settings_obj, key, default)
    return default
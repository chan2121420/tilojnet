from django import template
from django.core.cache import cache
from django.db.utils import OperationalError, ProgrammingError

register = template.Library()


@register.simple_tag
def get_site_settings():
    """Get site settings with caching"""
    try:
        settings = cache.get('site_settings')
        if settings is None:
            from core.models import SiteSettings
            settings = SiteSettings.objects.first()
            if settings:
                cache.set('site_settings', settings, 300)  # Cache for 5 minutes
        return settings
    except (OperationalError, ProgrammingError):
        return None
    except Exception:
        return None


@register.simple_tag
def get_nav_categories():
    """Get navigation categories with caching"""
    try:
        categories = cache.get('nav_categories')
        if categories is None:
            from services.models import ServiceCategory
            categories = list(ServiceCategory.objects.all()[:6])
            cache.set('nav_categories', categories, 300)  # Cache for 5 minutes
        return categories
    except (OperationalError, ProgrammingError):
        return []
    except Exception:
        return []
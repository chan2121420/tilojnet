from core.models import SiteSettings
from services.models import ServiceCategory


def site_settings(request):
    """Make site settings available in all templates"""
    settings = None
    categories = []
    
    try:
        settings = SiteSettings.objects.first()
    except Exception as e:
        # Handle case where table doesn't exist yet (during migrations)
        print(f"Error loading site settings: {e}")
        settings = None
    
    try:
        categories = ServiceCategory.objects.all()[:6]
    except Exception as e:
        print(f"Error loading categories: {e}")
        categories = []
    
    return {
        'site_settings': settings,
        'nav_categories': categories,
    }
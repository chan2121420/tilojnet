from django.db.utils import OperationalError, ProgrammingError


def site_settings(request):
    """Make site settings available in all templates"""
    settings = None
    categories = []
    
    try:
        from core.models import SiteSettings
        settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError) as e:
        # Tables don't exist yet (during migration)
        print(f"SiteSettings table not ready: {e}")
        settings = None
    except Exception as e:
        # Other errors
        print(f"Error loading site settings: {e}")
        settings = None
    
    try:
        from services.models import ServiceCategory
        categories = ServiceCategory.objects.all()[:6]
    except (OperationalError, ProgrammingError) as e:
        # Tables don't exist yet (during migration)
        print(f"ServiceCategory table not ready: {e}")
        categories = []
    except Exception as e:
        # Other errors
        print(f"Error loading categories: {e}")
        categories = []
    
    return {
        'site_settings': settings,
        'nav_categories': categories,
    }
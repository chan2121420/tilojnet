from core.models import SiteSettings, ServiceCategory

def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.objects.first()
    except Exception as e:
        # Handle case where table doesn't exist yet (during migrations)
        settings = None
    
    try:
        categories = ServiceCategory.objects.all()[:6]
    except Exception:
        categories = []
    
    return {
        'site_settings': settings,
        'nav_categories': categories,
    }
from core.models import SiteSettings, ServiceCategory

def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    categories = ServiceCategory.objects.all()[:6]
    
    return {
        'site_settings': settings,
        'nav_categories': categories,
    }
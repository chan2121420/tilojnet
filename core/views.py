from django.shortcuts import render
from django.db.models import Count
from django.db.utils import ProgrammingError, OperationalError

from .models import HeroSlide, Testimonial, TeamMember
from services.models import ServiceCategory
from projects.models import Project


def home(request):
    """
    Home page view with optimized database queries
    Uses select_related and prefetch_related to avoid N+1 queries
    """
    # Safely get hero slides with error handling
    try:
        hero_slides = list(HeroSlide.objects.filter(is_active=True))
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load hero slides: {e}")
        hero_slides = []
    
    # Safely get featured categories
    try:
        featured_categories = list(
            ServiceCategory.objects
                          .filter(is_featured=True)
                          .annotate(item_count=Count('items'))
                          [:6]
        )
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load featured categories: {e}")
        featured_categories = []
    
    # Safely get all categories preview
    try:
        all_categories_preview = list(
            ServiceCategory.objects
                          .all()
                          .annotate(item_count=Count('items'))
                          [:8]
        )
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load categories preview: {e}")
        all_categories_preview = []
    
    # Safely get featured projects
    try:
        featured_projects = list(
            Project.objects
                  .filter(is_featured=True, is_published=True)
                  .select_related('category')
                  .prefetch_related('service_categories')
                  .only(
                      'id', 'slug', 'title', 'featured_image', 
                      'location', 'short_description', 'category'
                  )
                  [:6]
        )
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load featured projects: {e}")
        featured_projects = []
    
    # Safely get testimonials
    try:
        testimonials = list(
            Testimonial.objects
                      .filter(is_featured=True)
                      .only(
                          'client_name', 'client_position', 'client_company',
                          'client_image', 'rating', 'testimonial_text'
                      )
                      [:3]
        )
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load testimonials: {e}")
        testimonials = []
    
    # Safely get team members
    try:
        team_members = list(
            TeamMember.objects
                     .filter(is_active=True)
                     .only(
                         'name', 'position', 'image', 'specialization',
                         'years_experience', 'linkedin_url'
                     )
                     [:4]
        )
    except (ProgrammingError, OperationalError) as e:
        print(f"Warning: Could not load team members: {e}")
        team_members = []
    
    context = {
        'hero_slides': hero_slides,
        'featured_categories': featured_categories,
        'all_categories_preview': all_categories_preview,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'team_members': team_members,
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page with optimized queries
    """
    try:
        team_members = list(
            TeamMember.objects
                     .filter(is_active=True)
                     .only(
                         'name', 'position', 'image', 'bio',
                         'specialization', 'years_experience', 'linkedin_url'
                     )
        )
    except (ProgrammingError, OperationalError):
        team_members = []
    
    try:
        testimonials = list(
            Testimonial.objects
                      .all()
                      .only(
                          'client_name', 'client_position', 'client_company',
                          'client_image', 'rating', 'testimonial_text'
                      )
                      [:6]
        )
    except (ProgrammingError, OperationalError):
        testimonials = []
    
    context = {
        'team_members': team_members,
        'testimonials': testimonials,
    }
    
    return render(request, 'core/about.html', context)


def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
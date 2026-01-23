from django.shortcuts import render
from django.db.models import Count

from .models import HeroSlide, Testimonial, TeamMember
from services.models import ServiceCategory
from projects.models import Project


def home(request):
    """
    Home page view with optimized database queries
    Uses select_related and prefetch_related to avoid N+1 queries
    """
    context = {
        # Hero slides (simple query)
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        
        # Featured categories with item count annotation
        # No need for select_related here as we're just displaying category info
        'featured_categories': (
            ServiceCategory.objects
                          .filter(is_featured=True)
                          .annotate(item_count=Count('items'))
                          [:6]
        ),
        
        # All categories preview with item count
        'all_categories_preview': (
            ServiceCategory.objects
                          .all()
                          .annotate(item_count=Count('items'))
                          [:8]
        ),
        
        # Featured projects with optimized queries
        # Use select_related for ForeignKey (category)
        # Use prefetch_related for ManyToMany (service_categories)
        'featured_projects': (
            Project.objects
                  .filter(is_featured=True, is_published=True)
                  .select_related('category')
                  .prefetch_related('service_categories')
                  .only(
                      'id', 'slug', 'title', 'featured_image', 
                      'location', 'short_description', 'category'
                  )
                  [:6]
        ),
        
        # Featured testimonials (simple query with only needed fields)
        'testimonials': (
            Testimonial.objects
                      .filter(is_featured=True)
                      .only(
                          'client_name', 'client_position', 'client_company',
                          'client_image', 'rating', 'testimonial_text'
                      )
                      [:3]
        ),
        
        # Active team members (simple query with only needed fields)
        'team_members': (
            TeamMember.objects
                     .filter(is_active=True)
                     .only(
                         'name', 'position', 'image', 'specialization',
                         'years_experience', 'linkedin_url'
                     )
                     [:4]
        ),
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page with optimized queries
    """
    context = {
        # All active team members
        'team_members': (
            TeamMember.objects
                     .filter(is_active=True)
                     .only(
                         'name', 'position', 'image', 'bio',
                         'specialization', 'years_experience', 'linkedin_url'
                     )
        ),
        
        # Recent testimonials
        'testimonials': (
            Testimonial.objects
                      .all()
                      .only(
                          'client_name', 'client_position', 'client_company',
                          'client_image', 'rating', 'testimonial_text'
                      )
                      [:6]
        ),
    }
    
    return render(request, 'core/about.html', context)


def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
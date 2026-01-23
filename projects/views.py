from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F

from .models import Project, ProjectCategory


def projects_list(request):
    """
    Portfolio/projects listing with optimized queries
    Uses custom manager methods for clean, DRY code
    """
    # Start with published projects and optimize queries
    projects = Project.objects.published().with_related()
    
    # Get all categories for filter dropdown
    categories = ProjectCategory.objects.all()
    
    # Apply filters using manager methods
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        projects = projects.by_category(category_slug)
    
    if search_query:
        projects = projects.search(search_query)
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'projects/projects_list.html', context)


def project_detail(request, slug):
    """
    Individual project detail with optimized queries
    Increments view count atomically
    """
    # Optimize query with select_related and prefetch_related
    project = get_object_or_404(
        Project.objects.select_related('category')
                      .prefetch_related('service_categories', 'images'),
        slug=slug,
        is_published=True
    )
    
    # Increment views atomically (avoids race conditions)
    Project.objects.filter(pk=project.pk).update(views_count=F('views_count') + 1)
    # Refresh to get updated count
    project.refresh_from_db(fields=['views_count'])
    
    # Get related projects efficiently
    related_projects = (
        Project.objects.published()
                      .filter(category=project.category)
                      .exclude(id=project.id)
                      .select_related('category')
                      .only('id', 'slug', 'title', 'featured_image', 'location', 'category')
                      [:3]
    )
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)
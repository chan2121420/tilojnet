from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F

from .models import Project, ProjectCategory


def projects_list(request):
    projects = Project.objects.published().with_related()
    
    categories = ProjectCategory.objects.all()
    
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    if search_query:
        projects = projects.search(search_query)
    
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'core/projects_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('category')
                      .prefetch_related('service_categories', 'images'),
        slug=slug,
        is_published=True
    )
    
    Project.objects.filter(pk=project.pk).update(views_count=F('views_count') + 1)
    project.refresh_from_db(fields=['views_count'])
    
    related_projects = (
        Project.objects.filter(is_published=True, category=project.category)
                      .exclude(id=project.id)
                      .select_related('category')
                      .only('id', 'slug', 'title', 'featured_image', 'location', 'category')
                      [:3]
    )
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'core/project_detail.html', context)
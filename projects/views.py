from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import *

def projects_list(request):
    """Portfolio/projects listing"""
    projects = Project.objects.filter(is_published=True)
    categories = ProjectCategory.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
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
    """Individual project detail"""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Increment views
    project.views_count += 1
    project.save(update_fields=['views_count'])
    
    # Get related projects
    related_projects = Project.objects.filter(
        category=project.category,
        is_published=True
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, ServiceCategory
from projects.models import Project 

def services_list(request):
    """All services page"""
    categories = ServiceCategory.objects.all()
    services = Service.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        services = services.filter(category__slug=category_slug)
    
    context = {
        'categories': categories,
        'services': services,
        'active_category': category_slug,
    }
    return render(request, 'services/services_list.html', context)


def service_detail(request, slug):
    """Individual service page"""
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.filter(category=service.category).exclude(id=service.id)[:3]
    related_projects = Project.objects.filter(
        is_published=True
    )[:4]  # You can add service-to-project relationships
    
    context = {
        'service': service,
        'related_services': related_services,
        'related_projects': related_projects,
    }
    return render(request, 'services/service_detail.html', context)
def categories_list(request):
    categories = ServiceCategory.objects.all().values("id", "name")
    return JsonResponse(list(categories), safe=False)


def search_categories(request):
    query = request.GET.get("q", "")
    categories = ServiceCategory.objects.filter(name__icontains=query).values("id", "name")
    return JsonResponse(list(categories), safe=False)

def category_detail(request, slug):
    try:
        category = ServiceCategory.objects.get(slug=slug)
    except ServiceCategory.DoesNotExist:
        raise Http404("Category not found")

    data = {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description if hasattr(category, "description") else "",
    }

    return JsonResponse(data)

def category_item_detail(request, category_slug, item_slug):
    try:
        category = ServiceCategory.objects.get(slug=category_slug)
    except ServiceCategory.DoesNotExist:
        raise Http404("Category not found")

    try:
        item = Service.objects.get(slug=item_slug, category=category)
    except Service.DoesNotExist:
        raise Http404("Item not found in this category")

    data = {
        "id": item.id,
        "title": item.title,
        "slug": item.slug,
        "category": category.name,
        "short_description": item.short_description,
        "full_description": item.full_description,
    }
    return JsonResponse(data)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from .models import ServiceCategory, CategoryItem
from projects.models import Project


def categories_list(request):
    categories = ServiceCategory.objects.all().annotate(
        item_count=Count('items'),
        project_count=Count('projects')
    )
    context = {'categories': categories}
    return render(request, 'core/categories_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    items = CategoryItem.objects.filter(category=category)
    
    style_filter = request.GET.get('style')
    if style_filter:
        items = items.filter(design_styles__contains=[style_filter])
    
    all_styles = set()
    for item in CategoryItem.objects.filter(category=category):
        if item.design_styles:
            all_styles.update(item.design_styles)
    
    related_projects = Project.objects.filter(
        service_categories=category, 
        is_published=True
    )[:4]
    
    popular_items = items.filter(is_popular=True)[:3]
    
    context = {
        'category': category,
        'items': items,
        'popular_items': popular_items,
        'related_projects': related_projects,
        'all_styles': sorted(all_styles),
        'active_style': style_filter,
    }
    return render(request, 'core/category_detail.html', context)


def category_item_detail(request, category_slug, item_slug):
    category = get_object_or_404(ServiceCategory, slug=category_slug)
    item = get_object_or_404(CategoryItem, category=category, slug=item_slug)
    
    related_items = CategoryItem.objects.filter(
        category=category
    ).exclude(id=item.id)[:4]
    
    related_projects = Project.objects.filter(
        service_categories=category, 
        is_published=True
    )[:3]
    
    context = {
        'category': category,
        'item': item,
        'related_items': related_items,
        'related_projects': related_projects,
    }
    return render(request, 'core/category_item_detail.html', context)


def search_categories(request):
    query = request.GET.get('q', '')
    
    categories = ServiceCategory.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    
    items = CategoryItem.objects.filter(
        Q(name__icontains=query) | 
        Q(short_description__icontains=query) | 
        Q(full_description__icontains=query)
    )
    
    context = {
        'query': query,
        'categories': categories,
        'items': items,
        'total_results': categories.count() + items.count(),
    }
    return render(request, 'core/search_results.html', context)
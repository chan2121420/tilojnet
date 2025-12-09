from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from .models import *

def home(request):
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'featured_categories': ServiceCategory.objects.filter(is_featured=True).annotate(item_count=Count('items'))[:6],
        'all_categories_preview': ServiceCategory.objects.all().annotate(item_count=Count('items'))[:8],
        'featured_projects': Project.objects.filter(is_featured=True, is_published=True)[:6],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:3],
        'team_members': TeamMember.objects.filter(is_active=True)[:4],
    }
    return render(request, 'core/home.html', context)

def about(request):
    context = {
        'team_members': TeamMember.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.all()[:6],
    }
    return render(request, 'core/about.html', context)

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
    related_projects = Project.objects.filter(service_categories=category, is_published=True)[:4]
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
    related_items = CategoryItem.objects.filter(category=category).exclude(id=item.id)[:4]
    related_projects = Project.objects.filter(service_categories=category, is_published=True)[:3]
    context = {
        'category': category,
        'item': item,
        'related_items': related_items,
        'related_projects': related_projects,
    }
    return render(request, 'core/category_item_detail.html', context)

def search_categories(request):
    query = request.GET.get('q', '')
    categories = ServiceCategory.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    items = CategoryItem.objects.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(full_description__icontains=query))
    context = {
        'query': query,
        'categories': categories,
        'items': items,
        'total_results': categories.count() + items.count(),
    }
    return render(request, 'core/search_results.html', context)

def projects_list(request):
    projects = Project.objects.filter(is_published=True)
    categories = ProjectCategory.objects.all()
    service_categories = ServiceCategory.objects.all()
    category_slug = request.GET.get('category')
    service_cat_slug = request.GET.get('service_category')
    search_query = request.GET.get('q')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    if service_cat_slug:
        projects = projects.filter(service_categories__slug=service_cat_slug)
    if search_query:
        projects = projects.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query) | Q(location__icontains=search_query))
    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'projects': page_obj,
        'categories': categories,
        'service_categories': service_categories,
        'active_category': category_slug,
        'active_service_category': service_cat_slug,
        'search_query': search_query,
    }
    return render(request, 'core/projects_list.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    project.views_count += 1
    project.save(update_fields=['views_count'])
    related_projects = Project.objects.filter(category=project.category, is_published=True).exclude(id=project.id)[:3]
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'core/project_detail.html', context)

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        try:
            send_mail(
                f'New Contact: {request.POST.get("subject")}',
                f'From: {request.POST.get("name")} ({request.POST.get("email")})\nPhone: {request.POST.get("phone")}\n\n{request.POST.get("message")}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except:
            pass
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    categories = ServiceCategory.objects.all()
    return render(request, 'core/contact.html', {'categories': categories})

def quote_request(request):
    categories = ServiceCategory.objects.all()
    if request.method == 'POST':
        quote = QuoteRequest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            service_category_id=request.POST.get('service_category') if request.POST.get('service_category') else None,
            location=request.POST.get('location'),
            budget=request.POST.get('budget'),
            project_description=request.POST.get('project_description'),
            timeline=request.POST.get('timeline'),
        )
        selected_items = request.POST.getlist('category_items')
        if selected_items:
            quote.category_items.set(selected_items)
        try:
            category_name = ServiceCategory.objects.get(id=request.POST.get('service_category')).name if request.POST.get('service_category') else "General"
            send_mail(
                f'New Quote Request - {category_name}',
                f'From: {request.POST.get("name")} ({request.POST.get("email")})\nPhone: {request.POST.get("phone")}\nLocation: {request.POST.get("location")}\nBudget: {request.POST.get("budget")}\n\n{request.POST.get("project_description")}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except:
            pass
        messages.success(request, 'Your quote request has been submitted! We will contact you within 24 hours.')
        return redirect('quote_request')
    return render(request, 'core/quote_request.html', {'categories': categories})

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            Newsletter.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)
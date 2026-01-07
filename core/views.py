from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from .models import SiteSettings, HeroSlide, Testimonial, TeamMember
from services.models import ServiceCategory, CategoryItem
from projects.models import Project, ProjectCategory
from contact.models import ContactMessage, QuoteRequest, Newsletter


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


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)
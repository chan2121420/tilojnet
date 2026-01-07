from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, QuoteRequest, Newsletter
from services.models import ServiceCategory


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text
        )
        
        # Send email notification
        try:
            send_mail(
                f'New Contact Form: {subject}',
                f'From: {name} ({email})\nPhone: {phone}\n\nMessage:\n{message_text}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except:
            pass
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'core/contact.html')


def quote_request(request):
    """Quote request page"""
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
    """Newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            Newsletter.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    return redirect('home')


# ============= ERROR VIEWS =============

def custom_404(request, exception):
    """Custom 404 page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 page"""
    return render(request, 'errors/500.html', status=500)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import *

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
    
    return render(request, 'contact/contact.html')


def quote_request(request):
    """Quote request page"""
    if request.method == 'POST':
        QuoteRequest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            service_type=request.POST.get('service_type'),
            location=request.POST.get('location'),
            budget=request.POST.get('budget'),
            project_description=request.POST.get('project_description'),
            timeline=request.POST.get('timeline'),
        )
        
        messages.success(request, 'Your quote request has been submitted! We will contact you within 24 hours.')
        return redirect('quote_request')
    
    return render(request, 'contact/quote_request.html')


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
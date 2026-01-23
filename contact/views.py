from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, QuoteRequestForm, NewsletterForm
from .services import ContactService, QuoteService
from .models import Newsletter
from services.models import ServiceCategory


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page with form validation"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Create contact message using service
            contact_message = ContactService.create_contact_message(form.cleaned_data)
            
            # Send email notification (non-blocking)
            email_sent = ContactService.send_contact_notification(contact_message)
            
            if not email_sent:
                # Log warning but don't fail the request
                messages.warning(
                    request,
                    'Your message was saved but email notification failed. We will still review it.'
                )
            
            messages.success(
                request,
                'Thank you for your message! We will get back to you soon.'
            )
            return redirect('contact')
        else:
            # Form has validation errors
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})


@require_http_methods(["GET", "POST"])
def quote_request(request):
    """Quote request page with enhanced validation"""
    categories = ServiceCategory.objects.all()
    
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        
        if form.is_valid():
            # Create quote request using service
            quote = QuoteService.create_quote_request(form.cleaned_data)
            
            # Send notifications
            admin_notified = QuoteService.send_quote_notification(quote)
            customer_notified = QuoteService.send_quote_confirmation(quote)
            
            if not admin_notified:
                messages.warning(
                    request,
                    'Your quote request was saved but admin notification failed. We will still process it.'
                )
            
            messages.success(
                request,
                'Your quote request has been submitted! We will contact you within 24 hours.'
            )
            return redirect('quote_request')
        else:
            # Form has validation errors
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
    else:
        form = QuoteRequestForm()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'core/quote_request.html', context)


@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription with duplicate check"""
    email = request.POST.get('email', '').strip()
    
    if not email:
        messages.error(request, 'Please provide an email address.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    # Check if already subscribed
    if Newsletter.objects.filter(email=email).exists():
        messages.info(request, 'You are already subscribed to our newsletter.')
    else:
        # Create new subscription
        Newsletter.objects.create(email=email)
        messages.success(request, 'Thank you for subscribing to our newsletter!')
    
    # Redirect back to previous page or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ============= ERROR VIEWS =============

def custom_404(request, exception):
    """Custom 404 page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 page"""
    return render(request, 'errors/500.html', status=500)
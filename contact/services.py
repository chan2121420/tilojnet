from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

from .models import ContactMessage, QuoteRequest

logger = logging.getLogger(__name__)


class ContactService:
    """Service for handling contact message operations"""
    
    @staticmethod
    def create_contact_message(form_data):
        """
        Create a contact message from validated form data
        
        Args:
            form_data: Dictionary with validated contact data
            
        Returns:
            ContactMessage instance
        """
        return ContactMessage.objects.create(**form_data)
    
    @staticmethod
    def send_contact_notification(contact_message):
        """
        Send email notification for new contact message
        
        Args:
            contact_message: ContactMessage instance
            
        Returns:
            Boolean indicating success
        """
        try:
            subject = f'New Contact Form: {contact_message.subject}'
            message = (
                f'From: {contact_message.name} ({contact_message.email})\n'
                f'Phone: {contact_message.phone}\n\n'
                f'Message:\n{contact_message.message}'
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            logger.info(f"Contact notification sent for: {contact_message.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact notification: {str(e)}")
            return False


class QuoteService:
    """Service for handling quote request operations"""
    
    @staticmethod
    def create_quote_request(form_data):
        """
        Create a quote request from validated form data
        
        Args:
            form_data: Dictionary with validated quote data
            
        Returns:
            QuoteRequest instance
        """
        # Extract category_items for many-to-many relationship
        category_items = form_data.pop('category_items', [])
        
        # Create the quote request
        quote = QuoteRequest.objects.create(**form_data)
        
        # Set category items if any
        if category_items:
            quote.category_items.set(category_items)
        
        return quote
    
    @staticmethod
    def send_quote_notification(quote_request):
        """
        Send email notification for new quote request
        
        Args:
            quote_request: QuoteRequest instance
            
        Returns:
            Boolean indicating success
        """
        try:
            # Get category name safely
            category_name = (
                quote_request.service_category.name 
                if quote_request.service_category 
                else "General"
            )
            
            # Get selected items
            selected_items = quote_request.category_items.all()
            items_list = ', '.join([item.name for item in selected_items]) if selected_items else "None"
            
            subject = f'New Quote Request - {category_name}'
            message = (
                f'From: {quote_request.name} ({quote_request.email})\n'
                f'Phone: {quote_request.phone}\n'
                f'Location: {quote_request.location}\n'
                f'Service Category: {category_name}\n'
                f'Selected Items: {items_list}\n'
                f'Budget: {quote_request.get_budget_display()}\n'
                f'Timeline: {quote_request.timeline}\n\n'
                f'Project Description:\n{quote_request.project_description}'
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            logger.info(f"Quote notification sent for: {quote_request.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send quote notification: {str(e)}")
            return False
    
    @staticmethod
    def send_quote_confirmation(quote_request):
        """
        Send confirmation email to customer
        
        Args:
            quote_request: QuoteRequest instance
            
        Returns:
            Boolean indicating success
        """
        try:
            subject = 'Quote Request Received - Tilojnet Exclusive'
            message = (
                f'Dear {quote_request.name},\n\n'
                f'Thank you for your interest in Tilojnet Exclusive!\n\n'
                f'We have received your quote request and will review it carefully. '
                f'Our team will contact you within 24 hours to discuss your project in detail.\n\n'
                f'Your Request Summary:\n'
                f'Service Category: {quote_request.service_category.name if quote_request.service_category else "General"}\n'
                f'Location: {quote_request.location}\n'
                f'Budget Range: {quote_request.get_budget_display()}\n\n'
                f'If you have any urgent questions, please don\'t hesitate to contact us.\n\n'
                f'Best regards,\n'
                f'The Tilojnet Exclusive Team'
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quote_request.email],
                fail_silently=True,  # Don't fail if customer email fails
            )
            
            logger.info(f"Quote confirmation sent to: {quote_request.email}")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to send quote confirmation: {str(e)}")
            return False
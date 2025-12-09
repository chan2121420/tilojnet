from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from services.models import ServiceCategory, CategoryItem

class ContactMessage(models.Model):
    """Contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class QuoteRequest(models.Model):
    """Quote/consultation requests"""
    BUDGET_CHOICES = [
        ('under_5k', 'Under $5,000'),
        ('5k_10k', '$5,000 - $10,000'),
        ('10k_25k', '$10,000 - $25,000'),
        ('25k_50k', '$25,000 - $50,000'),
        ('50k_100k', '$50,000 - $100,000'),
        ('over_100k', 'Over $100,000'),
        ('flexible', 'Flexible'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    category_items = models.ManyToManyField(CategoryItem, blank=True, help_text="Specific items interested in")
    location = models.CharField(max_length=200)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    project_description = models.TextField()
    timeline = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.service_category if self.service_category else 'General'}"


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
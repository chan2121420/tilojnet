from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Tilojnet Exclusive")
    tagline = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='site/')
    favicon = models.ImageField(upload_to='site/', blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20)
    about_short = models.TextField()
    about_full = RichTextField()
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    meta_description = models.TextField()
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name


class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    image = models.ImageField(upload_to='hero/')
    cta_text = models.CharField(max_length=50, default="Get Started")
    cta_link = models.CharField(max_length=200, default="#contact")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True)
    client_company = models.CharField(max_length=100, blank=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    testimonial_text = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
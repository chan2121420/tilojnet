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


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    featured_image = models.ImageField(upload_to='categories/')
    banner_image = models.ImageField(upload_to='categories/banners/', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Service Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    short_description = models.TextField(max_length=300)
    full_description = RichTextField()
    featured_image = models.ImageField(upload_to='category_items/')
    price_range = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    ideal_space_size = models.CharField(max_length=100, blank=True)
    key_features = models.JSONField(default=list)
    materials_used = models.JSONField(default=list, blank=True)
    design_styles = models.JSONField(default=list, blank=True)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Category Items"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class CategoryItemImage(models.Model):
    item = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='category_items/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.item.name} - Image {self.order}"


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_categories')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Project Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('planned', 'Planned'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    service_categories = models.ManyToManyField(ServiceCategory, blank=True, related_name='projects')
    client_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    project_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    short_description = models.TextField(max_length=300)
    full_description = RichTextField()
    challenge = RichTextField(blank=True)
    solution = RichTextField(blank=True)
    result = RichTextField(blank=True)
    featured_image = models.ImageField(upload_to='projects/')
    budget_range = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tags = models.JSONField(default=list)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-project_date', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class ContactMessage(models.Model):
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
    category_items = models.ManyToManyField(CategoryItem, blank=True)
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
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
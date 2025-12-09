from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from services.models import ServiceCategory


class ProjectCategory(models.Model):
    """Project categories - can link to service categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    service_category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='project_categories'
    )
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
    """Portfolio projects"""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True,
        related_name='projects'
    )
    service_categories = models.ManyToManyField(
        ServiceCategory, blank=True, related_name='projects',
        help_text="Which service categories are featured in this project"
    )

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
    """Project gallery images"""
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"

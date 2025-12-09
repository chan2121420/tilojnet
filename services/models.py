from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class ServiceCategory(models.Model):
    """Main service categories like Kitchens, Ceilings, Bedrooms, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    icon = models.CharField(max_length=50, help_text="Font Awesome icon class, e.g., fa-utensils")
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

    def get_item_count(self):
        return self.items.count()


class CategoryItem(models.Model):
    """Individual items under each category"""
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


class Service(models.Model):
    """High-level services offered by the company"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.CharField(max_length=300)
    full_description = RichTextField()

    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='services/', blank=True)

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services'
    )

    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

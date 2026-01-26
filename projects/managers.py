from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)
    
    def featured(self):
        return self.filter(is_featured=True)
    
    def by_status(self, status):
        return self.filter(status=status)
    
    def by_category(self, category_slug):
        return self.filter(category__slug=category_slug)
    
    def by_service_category(self, service_category_slug):
        return self.filter(service_categories__slug=service_category_slug)
    
    def search(self, query):
        if not query:
            return self
        
        return self.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(location__icontains=query) |
            Q(client_name__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
    
    def with_related(self):
        return self.select_related(
            'category'
        ).prefetch_related(
            'service_categories',
            'images'
        )
    
    def recent(self, limit=10):
        return self.order_by('-project_date', '-created_at')[:limit]
    
    def popular(self, limit=10):
        return self.order_by('-views_count')[:limit]


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def by_category(self, category_slug):
        return self.get_queryset().by_category(category_slug)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
    def with_related(self):
        return self.get_queryset().with_related()
from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):
    """Custom QuerySet for Project model with chainable filters"""
    
    def published(self):
        """Filter only published projects"""
        return self.filter(is_published=True)
    
    def featured(self):
        """Filter featured projects"""
        return self.filter(is_featured=True)
    
    def by_status(self, status):
        """
        Filter projects by status
        
        Args:
            status: One of 'completed', 'ongoing', 'planned'
        """
        return self.filter(status=status)
    
    def by_category(self, category_slug):
        """
        Filter projects by category slug
        
        Args:
            category_slug: The slug of the ProjectCategory
        """
        return self.filter(category__slug=category_slug)
    
    def by_service_category(self, service_category_slug):
        """
        Filter projects by service category slug
        
        Args:
            service_category_slug: The slug of the ServiceCategory
        """
        return self.filter(service_categories__slug=service_category_slug)
    
    def search(self, query):
        """
        Search projects by title, description, or location
        
        Args:
            query: Search string
        """
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
        """Optimize queries by prefetching related objects"""
        return self.select_related(
            'category'
        ).prefetch_related(
            'service_categories',
            'images'
        )
    
    def recent(self, limit=10):
        """Get most recent projects by date"""
        return self.order_by('-project_date', '-created_at')[:limit]
    
    def popular(self, limit=10):
        """Get most viewed projects"""
        return self.order_by('-views_count')[:limit]


class ProjectManager(models.Manager):
    """Custom manager for Project model"""
    
    def get_queryset(self):
        """Override default queryset to use ProjectQuerySet"""
        return ProjectQuerySet(self.model, using=self._db)
    
    def published(self):
        """Shortcut for published projects"""
        return self.get_queryset().published()
    
    def featured(self):
        """Shortcut for featured projects"""
        return self.get_queryset().featured()
    
    def by_category(self, category_slug):
        """Shortcut for filtering by category"""
        return self.get_queryset().by_category(category_slug)
    
    def search(self, query):
        """Shortcut for search"""
        return self.get_queryset().search(query)
    
    def with_related(self):
        """Shortcut for optimized queries"""
        return self.get_queryset().with_related()
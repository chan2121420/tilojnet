from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Clear site settings and navigation cache'

    def handle(self, *args, **options):
        cache.delete('site_settings')
        cache.delete('nav_categories')
        self.stdout.write(self.style.SUCCESS('Successfully cleared site cache'))
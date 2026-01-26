from django.core.management.base import BaseCommand
from django.db.utils import ProgrammingError, OperationalError
from core.models import HeroSlide


class Command(BaseCommand):
    help = 'Initialize default hero slides if none exist'

    def handle(self, *args, **options):
        try:
            if HeroSlide.objects.exists():
                self.stdout.write(
                    self.style.SUCCESS('✅ Hero slides already exist')
                )
                return
            
            # Create default hero slides
            slides_data = [
                {
                    'title': 'Transform Your Space',
                    'subtitle': 'Premium Interior Design Solutions for Modern Living',
                    'image': 'hero/default-1.jpg',
                    'cta_text': 'Get Started',
                    'cta_link': '/quote/',
                    'order': 1,
                    'is_active': True
                },
                {
                    'title': 'Exceptional Design Excellence',
                    'subtitle': 'Creating Beautiful, Functional Spaces That Inspire',
                    'image': 'hero/default-2.jpg',
                    'cta_text': 'View Portfolio',
                    'cta_link': '/projects/',
                    'order': 2,
                    'is_active': True
                },
                {
                    'title': 'Your Dream Space Awaits',
                    'subtitle': 'Expert Designers Ready to Bring Your Vision to Life',
                    'image': 'hero/default-3.jpg',
                    'cta_text': 'Contact Us',
                    'cta_link': '/contact/',
                    'order': 3,
                    'is_active': True
                },
            ]
            
            for slide_data in slides_data:
                HeroSlide.objects.create(**slide_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully created {len(slides_data)} default hero slides')
            )
            
        except (ProgrammingError, OperationalError) as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating hero slides: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Unexpected error: {str(e)}')
            )
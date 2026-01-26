from django.core.management.base import BaseCommand
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
            # Note: You'll need to manually upload images to Supabase later
            # For now, we'll use placeholder paths
            HeroSlide.objects.create(
                title="Transform Your Space",
                subtitle="Premium Interior Design Solutions for Modern Living",
                image="hero/placeholder-hero-1.jpg",
                cta_text="Get Started",
                cta_link="/quote/",
                order=1,
                is_active=True
            )
            
            HeroSlide.objects.create(
                title="Exceptional Design Excellence",
                subtitle="Creating Beautiful, Functional Spaces That Inspire",
                image="hero/placeholder-hero-2.jpg",
                cta_text="View Portfolio",
                cta_link="/projects/",
                order=2,
                is_active=True
            )
            
            HeroSlide.objects.create(
                title="Your Dream Space Awaits",
                subtitle="Expert Designers Ready to Bring Your Vision to Life",
                image="hero/placeholder-hero-3.jpg",
                cta_text="Contact Us",
                cta_link="/contact/",
                order=3,
                is_active=True
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Successfully created default hero slides')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating hero slides: {str(e)}')
            )
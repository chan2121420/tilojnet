from django.core.management.base import BaseCommand
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize default site settings if none exist'

    def handle(self, *args, **options):
        try:
            if SiteSettings.objects.exists():
                self.stdout.write(
                    self.style.SUCCESS('✅ Site settings already exist')
                )
                return
            
            # Create default settings
            SiteSettings.objects.create(
                site_name="Tilojnet Exclusive",
                tagline="Premium Interior Design Services",
                phone="+263 771 234 567",
                email="info@tilojnet.com",
                address="123 Design Street, Harare, Zimbabwe",
                whatsapp_number="263771234567",
                about_short="We are a premium interior design company dedicated to transforming spaces into stunning, functional environments.",
                about_full="""
                <p>At Tilojnet Exclusive, we believe every space tells a story. Our expert team combines creativity, 
                functionality, and your vision to create stunning environments that reflect your unique style and personality.</p>
                <p>With over 10 years of experience and 100+ completed projects, we're committed to delivering excellence in every detail.</p>
                """,
                meta_description="Tilojnet Exclusive offers premium interior design services for residential and commercial spaces in Zimbabwe. Transform your space with our expert designers.",
                mission="To transform ordinary spaces into extraordinary experiences through innovative design and exceptional craftsmanship.",
                vision="To be Zimbabwe's leading interior design company, known for creativity, quality, and client satisfaction."
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Successfully created default site settings')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating site settings: {str(e)}')
            )
#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==================================="
echo "Starting Build Process..."
echo "==================================="

echo "Step 1: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Step 2: Collecting static files..."
python manage.py collectstatic --no-input

echo "Step 3: Running migrations..."
# Run migrations for all apps
python manage.py migrate --noinput

echo "Step 4: Creating default site settings..."
python manage.py shell << 'EOF'
from core.models import SiteSettings
try:
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            site_name="Tilojnet Exclusive",
            tagline="Premium Interior Design Services",
            phone="+263 771 234 567",
            email="info@tilojnet.com",
            address="123 Design Street, Harare, Zimbabwe",
            whatsapp_number="263771234567",
            about_short="We are a premium interior design company dedicated to transforming spaces into stunning, functional environments.",
            about_full="<p>At Tilojnet Exclusive, we believe every space tells a story. Our expert team combines creativity, functionality, and your vision to create stunning environments that reflect your unique style and personality.</p><p>With over 10 years of experience and 100+ completed projects, we're committed to delivering excellence in every detail.</p>",
            meta_description="Tilojnet Exclusive offers premium interior design services for residential and commercial spaces in Zimbabwe. Transform your space with our expert designers.",
            mission="To transform ordinary spaces into extraordinary experiences through innovative design and exceptional craftsmanship.",
            vision="To be Zimbabwe's leading interior design company, known for creativity, quality, and client satisfaction."
        )
        print("✅ Created default site settings successfully")
    else:
        print("✅ Site settings already exist")
except Exception as e:
    print(f"❌ Error creating site settings: {e}")
EOF

echo "==================================="
echo "Build completed successfully!"
echo "==================================="
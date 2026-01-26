#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==================================="
echo "Starting Build Process..."
echo "==================================="

echo "Step 1: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Step 2: Running migrations..."
# Run migrations multiple times with different flags to ensure tables are created
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput
python manage.py migrate --run-syncdb --noinput

echo "Step 3: Collecting static files..."
python manage.py collectstatic --no-input

echo "Step 4: Initializing site data..."
python manage.py init_site_settings || echo "Warning: Could not initialize site settings"
python manage.py init_hero_slides || echo "Warning: Could not initialize hero slides"

echo "==================================="
echo "Build completed successfully!"
echo "==================================="
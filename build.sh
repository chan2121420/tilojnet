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
# First, try normal migrations
python manage.py migrate --noinput

# Then force create any missing tables
echo "Step 2b: Ensuring all tables exist..."
python manage.py migrate --run-syncdb

echo "Step 3: Initializing site data..."
python manage.py init_site_settings
python manage.py init_hero_slides

echo "Step 4: Collecting static files..."
python manage.py collectstatic --no-input

echo "==================================="
echo "Build completed successfully!"
echo "==================================="
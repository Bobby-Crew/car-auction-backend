#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
python manage.py createsuperuser --noinput

# Create logs directory if it doesn't exist
mkdir -p logs 
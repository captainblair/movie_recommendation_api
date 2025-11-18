#!/bin/bash

# Movie Recommendation API Setup Script
# This script sets up the development environment

set -e

echo "=========================================="
echo "Movie Recommendation API - Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your configuration."
else
    echo ".env file already exists."
fi

# Create logs directory
echo ""
echo "Creating logs directory..."
mkdir -p logs

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run tests
echo ""
echo "Running tests..."
python manage.py test --verbosity 2

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Visit http://localhost:8000/api/docs/ for API documentation"
echo "3. Visit http://localhost:8000/admin/ for Django admin"
echo ""

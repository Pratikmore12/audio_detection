#!/bin/bash

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: username=admin, password=admin123")
else:
    print("Superuser already exists")
EOF

# Start the server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 
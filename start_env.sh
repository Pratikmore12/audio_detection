#!/bin/bash

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if environment variables are set
if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_EMAIL" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser with environment variables..."
    python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print("Superuser created: username=$DJANGO_SUPERUSER_USERNAME")
else:
    print("Superuser $DJANGO_SUPERUSER_USERNAME already exists")
EOF
else
    echo "Environment variables not set for superuser creation. Skipping..."
fi

# Start the server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 
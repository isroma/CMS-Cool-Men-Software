#!/bin/bash

# Create superuser if it doesnt exists on database
echo "----- Create superuser if necessary -----"
python manage.py initadmin --username=admin --email=admin@example.com --password=admin 

# Make database migrations before applying
echo "----- Make database migrations -----"
python manage.py makemigrations

# Apply database migrations
echo "----- Apply database migrations -----"
python manage.py migrate

# Antes de comenzar hay que reinicar los indices
echo "----- Rebuilding elasticsearch index -----"
python manage.py search_index --rebuild 

# Start server
echo "----- Starting server on port 5432 -----"
python manage.py runserver 0.0.0.0:5432
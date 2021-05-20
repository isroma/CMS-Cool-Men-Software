#!/bin/bash

# Apply CORS to SwiftStack
echo "----- Applying CORS -----"
swift -A "http://swiftstack:8080/auth/v1.0" -U test -K test post container -H "X-Container-Meta-Access-Control-Allow-Origin:*"

# Create superuser if it doesnt exists on database
echo "----- Create superuser if necessary -----"
python manage.py initadmin --username=admin --email=admin@example.com --password=admin 

# Make database migrations before applying
echo "----- Make database migrations -----"
yes | python manage.py makemigrations

# Apply database migrations
echo "----- Apply database migrations -----"
yes | python manage.py migrate

# Start server
echo "----- Starting server on port 5432 -----"
python manage.py runserver 0.0.0.0:5432
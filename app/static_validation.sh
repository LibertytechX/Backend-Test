#!/bin/bash

# Run black
echo "Running black..."
black core --line-length=90

# Run isort
echo "Running isort..."
isort core

# Run django migrations check to ensure that there are no migrations left to create
echo "Running makemigrations..."
python manage.py makemigrations

echo "Running migrate..."
python manage.py migrate

# run python static validation
echo "Running pylint"
pylint core

# Run mypy
echo "Running mypy..."
mypy core

# Run Test
echo "Running test..."
python manage.py test
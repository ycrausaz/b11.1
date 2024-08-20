# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install the postresql client to populate the database
RUN apt-get update && apt-get install -y postgresql-client

# Copy the entire application directory into the container at /app
COPY . /app/

# Create the directory for static files
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start the Django server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "LBA.wsgi:application", "--bind", "0.0.0.0:8000"]

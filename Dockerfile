# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client libpq-dev

# Copy requirements and install Python packages
COPY requirements.in /app/
RUN pip install --upgrade pip && pip install pip-tools
RUN pip-compile requirements.in && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 80
EXPOSE 80

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

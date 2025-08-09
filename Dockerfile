# Use official Python image as base
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Work directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for caching
COPY poll_project/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Ensure entrypoint script has Unix line endings & is executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Render will pass PORT; default to 8000
ENV PORT=8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install git and dvc dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create models directory and set permissions
RUN mkdir -p /app/models && \
    chmod -R 777 /app/models

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Remove existing .dvc directory and reinitialize DVC
RUN rm -rf .dvc && dvc init --no-scm -f

# Expose the port the app runs on
EXPOSE 8000

# Add a healthcheck to wait for model file
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD test -f /app/models/model.pkl || exit 1

# Command to run the API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 
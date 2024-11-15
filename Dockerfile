# Use an official Python runtime as the base image to ensure a consistent and up-to-date Python environment.
# The '3.9-slim' tag specifies the Python version and the 'slim' variant, which is a smaller image size.
FROM python:3.9-slim

# Set the working directory in the container to '/app'. This is where the project files will be copied and executed.
WORKDIR /app

# Install git and dvc dependencies. Git is required for version control, and DVC (Data Version Control) is used for data management.
# The 'apt-get update' command updates the package list, 'apt-get install' installs the required packages, and 'rm -rf /var/lib/apt/lists/*' removes the package list files to save space.
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for models and set its permissions to allow all users to read, write, and execute.
# This is necessary for the model files to be accessible by the application.
RUN mkdir -p /app/models && \
    chmod -R 777 /app/models

# Copy the 'requirements.txt' file, which lists the project's Python dependencies, into the container.
# Then, install these dependencies using pip with the '--no-cache-dir' option to avoid caching and '-r' option to read from the file.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container.
COPY . .

# Remove any existing '.dvc' directory and reinitialize DVC to manage data and models.
# The '--no-scm' option tells DVC not to use source control systems like Git, and '-f' forces the initialization.
RUN rm -rf .dvc && dvc init --no-scm -f

# Expose port 8000 to allow incoming requests to the API.
EXPOSE 8000

# Add a healthcheck to ensure the container is healthy by checking the existence of a model file.
# The healthcheck will run every 10 seconds, timeout after 5 seconds, start checking after 5 seconds, and retry up to 3 times.
# If the model file is not found, the container will be considered unhealthy and restarted.
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD test -f /app/models/model.pkl || exit 1

# Command to run the API using uvicorn, a fast and lightweight ASGI server.
# The command specifies the host, port, and the application module to run.
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 
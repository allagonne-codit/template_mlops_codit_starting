FROM apache/airflow:2.7.1

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /opt/airflow/db /opt/airflow/data/raw /opt/airflow/models && \
    chown -R airflow:root /opt/airflow

USER airflow

# Copy requirements file
COPY requirements.txt /requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /requirements.txt

# Create a .env file to set PYTHONPATH
RUN echo "PYTHONPATH=/opt/airflow:/opt/airflow/dags:/app" > /opt/airflow/.env
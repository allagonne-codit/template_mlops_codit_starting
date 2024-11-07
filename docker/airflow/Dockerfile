FROM apache/airflow:2.7.1

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create directory for requirements
RUN mkdir /requirements && \
    chown -R airflow:root /requirements

# Switch to airflow user for pip installations
USER airflow

# Copy requirements file
COPY --chown=airflow:root requirements.txt /requirements/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /requirements/requirements.txt

# No need to switch back to airflow user since we're already airflow user
FROM python:3.9-slim

WORKDIR /mlflow

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create directories with user-level permissions
RUN mkdir -p /mlflow/mlruns /mlflow/db && \
    chmod -R 777 /mlflow

COPY requirements.txt .
RUN pip install mlflow psycopg2-binary

EXPOSE 5000

# Simple startup script with relative paths
CMD mlflow server \
    --backend-store-uri sqlite:///db/mlflow.db \
    --default-artifact-root /mlflow/mlruns \
    --host 0.0.0.0 \
    --port 5000
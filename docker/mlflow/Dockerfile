FROM python:3.9-slim

WORKDIR /mlflow

# Install curl for healthcheck and sqlite3 for database
RUN apt-get update && \
    apt-get install -y curl sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /mlflow/mlruns /mlflow/db

COPY requirements.txt .
RUN pip install mlflow psycopg2-binary

# Create a non-root user
RUN useradd -m -u 50000 mlflow && \
    chown -R mlflow:mlflow /mlflow && \
    chmod -R 777 /mlflow

USER mlflow

EXPOSE 5000

# Initialize database at runtime
CMD sqlite3 /mlflow/db/mlflow.db ".databases" && \
    mlflow server \
    --backend-store-uri sqlite:///db/mlflow.db \
    --default-artifact-root /mlflow/mlruns \
    --host 0.0.0.0 \
    --port 5000
# MLOps Best Practices Demo Project

## What We're Building

This project sets up a complete MLOps environment using Docker containers. Think of containers as isolated boxes, each running a specific part of our application:

1. **MLflow Container** (Port 5000)
   - Tracks our machine learning experiments
   - Stores model performance metrics
   - Saves trained models
   
2. **FastAPI Container** (Port 8000)
   - Serves our ML model via API
   - Handles prediction requests
   - Provides model information

3. **Airflow Container** (Port 8080)
   - Schedules and runs our training pipeline
   - Monitors job status
   - Handles workflow automation

## What is Docker?

Docker is like a shipping container for software. It packages everything your application needs to run (code, dependencies, settings) into a standardized unit called a container. This ensures that your application works the same way everywhere.

## Accessing the Services

### 1. MLflow Dashboard
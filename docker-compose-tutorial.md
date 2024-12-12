# Docker and Docker Compose Tutorial Using MLOps Demo

## 1. Introduction to Docker Basics

### What is Docker?

As shown in the README.md:

## What is Docker?
Docker is like a shipping container for software. It packages everything your application needs to run (code, dependencies, settings) into a standardized unit called a container. This ensures that your application works the same way everywhere.

Key Docker Concepts:

* **Container**: A lightweight, standalone package that includes everything needed to run a piece of software
* **Image**: A template for creating containers
* **Dockerfile**: A script containing instructions to build a Docker image
* **Registry**: A repository for storing and sharing Docker images

**Additional Explanation:**
Docker containers provide a consistent, isolated environment for running applications, which helps to ensure that the application will work the same way across different computing environments. This is especially useful for deployment and scaling of applications, as the containers can be easily moved, copied, and run on different systems.

## 2. Understanding Our Project's Docker Setup

### Main Components

Our project uses three main containers (as shown in README.md):

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

**Additional Explanation:**
Separating the different components of the project into individual Docker containers helps to maintain a clear separation of concerns, improve scalability, and enhance the overall maintainability of the system.

### Why Multiple Containers?

* **Separation of Concerns**: Each container has a specific responsibility
* **Scalability**: Can scale individual components independently
* **Isolation**: Problems in one container don't affect others
* **Maintainability**: Easier to update and maintain individual components

**Additional Explanation:**
Using multiple Docker containers allows for better organization and management of the different components of the application. This approach makes it easier to scale individual parts of the system, update or replace specific components, and isolate any issues that may arise.

## 3. Analyzing Dockerfiles

### MLflow Container Example

Let's look at the MLflow Dockerfile:

```dockerfile
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
```

Key points to explain:

* Base image selection (python:3.9-slim)
* Working directory setup
* Dependency installation
* Security considerations (non-root user)
* Port exposure
* Volume mounting
* Health checks

**Additional Explanation:**
The Dockerfile defines the steps required to build the Docker image for the MLflow container. It specifies the base image, installs necessary dependencies, sets up the working directory, creates a non-root user for security, exposes the port, and defines the command to run the MLflow server.

## 4. Docker Compose Deep Dive

### Purpose of Docker Compose

* Manages multi-container applications
* Defines services, networks, and volumes in a single file
* Simplifies container orchestration

**Additional Explanation:**
Docker Compose is a tool that allows you to define and manage the entire application stack, including multiple containers, networks, and volumes, in a single configuration file. This simplifies the process of setting up and running a multi-service application, as Docker Compose handles the orchestration and coordination of the different components.

### Analyzing docker-compose.yml

Key sections to explain:

* **Services Definition**:

```yaml
services:
  # MLflow service
  mlflow:
    image: mlflow-server
    build:
      context: .
      dockerfile: docker/mlflow/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow/mlruns
      - mlflow_db:/mlflow/db
    environment:
      - BACKEND_STORE_URI=sqlite:///db/mlflow.db
      - ARTIFACT_ROOT=/mlflow/mlruns
    networks:
      - airflow_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
```

* **Networking**:

```yaml
networks:
  airflow_network:
    driver: bridge
```

* **Volumes**:

```yaml
volumes:
  airflow_db:
    driver: local
  mlflow_data:
    driver: local
  mlflow_db:
    driver: local
```

**Additional Explanation:**
The `docker-compose.yml` file defines the different services (containers) that make up the application, including the MLflow, FastAPI, and Airflow services. It also defines the networks and volumes that will be used by the containers, ensuring that they can communicate with each other and that data is persisted.

## 5. Container Communication

### How Containers Talk to Each Other

1. **Network Setup**: All containers are on `airflow_network`
2. **Service Discovery**: Containers can reference each other by service name
   * Example: MLflow is accessible at `http://mlflow:5000`
3. **Dependencies**: Using `depends_on` to ensure proper startup order

**Additional Explanation:**
The containers in the application communicate with each other through the `airflow_network` network. By using the service names defined in the `docker-compose.yml` file, the containers can discover and connect to each other. The `depends_on` configuration ensures that the necessary services are started in the correct order, preventing issues with startup dependencies.

## 6. Hands-on Exercises

### Exercise 1: Starting the Environment

```bash
# Build and start all containers
docker-compose up --build

# View running containers
docker ps

# Check container logs
docker logs <container_name>
```

**Additional Explanation:**
These commands demonstrate how to start the entire application environment using Docker Compose. The `up --build` command builds and starts all the containers defined in the `docker-compose.yml` file. The `docker ps` command shows the running containers, and `docker logs` allows you to inspect the logs of a specific container.

### Exercise 2: Container Management

```bash
# Stop specific container
docker-compose stop mlflow

# Start specific container
docker-compose start mlflow

# Remove all containers
docker-compose down

# Remove containers and volumes
docker-compose down -v
```

**Additional Explanation:**
These commands show how to manage the individual containers and the overall application environment. You can stop, start, and remove specific containers or the entire application using Docker Compose commands. The `down -v` command also removes any associated volumes, which is useful for cleaning up the development environment.

### Exercise 3: Accessing Services

* MLflow UI: `http://localhost:5000`
* FastAPI: `http://localhost:8000/docs`
* Airflow: `http://localhost:8080`

**Additional Explanation:**
These URLs demonstrate how to access the different services that are running in the Docker containers. By mapping the container ports to the host system, you can easily interact with the MLflow UI, FastAPI, and Airflow web interfaces.

## 7. Best Practices

1. **Image Optimization**
   * Use `.dockerignore` to exclude unnecessary files:
     ```
     .git
     .dvc
     **pycache**
     *.pyc
     venv/
     mlruns/
     airflow/logs/
     ```

2. **Security Considerations**
   * Run containers as non-root users
   * Use specific versions for base images
   * Implement health checks
   * Properly manage secrets

3. **Resource Management**
   * Set container resource limits
   * Monitor container performance
   * Clean up unused containers and images

**Additional Explanation:**
These best practices cover important aspects of working with Docker, such as optimizing Docker image size, ensuring security, and managing resources effectively. Using a `.dockerignore` file to exclude unnecessary files can significantly reduce the size of the Docker images, making them faster to build and deploy. Running containers as non-root users, using specific version tags for base images, and implementing health checks help improve the overall security of the application. Properly managing container resources, monitoring performance, and cleaning up unused containers and images contribute to the long-term maintainability and efficiency of the Docker-based application.

## 8. Troubleshooting Common Issues

### Container Won't Start

```bash
# Check logs
docker logs <container_name>

# Inspect container
docker inspect <container_name>
```

**Additional Explanation:**
If a container fails to start, the first step is to check the container logs using the `docker logs` command. This will provide insights into any errors or issues that are preventing the container from starting. The `docker inspect` command can also be helpful in diagnosing container-related problems by providing detailed information about the container's configuration and state.

### Network Issues

```bash
# Inspect network
docker network ls
docker network inspect airflow_network
```

**Additional Explanation:**
Network-related issues can also arise when working with Docker-based applications. The `docker network ls` command can be used to list all the available networks, and the `docker network inspect` command can provide detailed information about a specific network, such as the connected containers and their IP addresses. This can help you identify and resolve any network connectivity problems between the containers.

### Volume Problems

```bash
# List volumes
docker volume ls

# Clean up volumes
docker volume prune
```

**Additional Explanation:**
Docker volumes are used to persist data between container runs, but issues can sometimes arise with these volumes. The `docker volume ls` command can be used to list all the available volumes, and the `docker volume prune` command can be used to clean up any unused volumes. This can be helpful in situations where volumes are not being properly cleaned up or are causing issues with the application.

This structure provides a comprehensive introduction to Docker and Docker Compose using your MLOps project as a practical example, with additional explanations to better explain the key concepts and usage of these tools.


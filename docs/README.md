# MLOps Project Setup Guide

## Introduction

This guide will walk you through transforming Jupyter notebooks into a structured MLOps project. We'll cover best practices, including setting up version control, organizing your code, and using tools like DVC for data versioning.

## Table of Contents

1. [Set Up the Environment](#set-up-the-environment)
    - [Project Structure](#project-structure)
    - [Create a Python Virtual Environment](#create-a-python-virtual-environment)
    - [Version Control with Git](#version-control-with-git)
    - [Basic Git Commands](#basic-git-commands)
    - [Data Versioning with DVC](#data-versioning-with-dvc)
2. [Transforming Jupyter Notebooks](#transforming-jupyter-notebooks)
    - [Organize Code into Functions](#organize-code-into-functions)
    - [Example Transformation](#example-transformation)
    - [Document the Process](#document-the-process)
    - [Detailed Explanation of Key Python Files](#detailed-explanation-of-key-python-files)
3. [API Development](#api-development)
    - [FastAPI Overview](#fastapi-overview)
    - [Key Features](#key-features)
    - [Example API structure](#example-api-structure)
    - [Key Endpoints](#key-endpoints)
    - [Running the API](#running-the-api)
4. [Docker in MLOps Projects](#docker-in-mlops-projects)
   - [What We are Building](#what-we-are-building)
   - [What is Docker?](#what-is-docker)
   - [Docker in This Project](#docker-in-this-project)


## Set up the environment

### Project Structure

Get the project structure from the provided zip file
It should look like this:
  ```sh
    project-root/
    │
    ├── data/                   # Data files
    │   ├── raw/                # Raw data
    │   └── processed/          # Processed data
    │
    ├── models/                 # Trained models
    │
    ├── notebooks/              # Jupyter notebooks
    │
    ├── src/                    # Source code
    │   ├── data/               # Data processing scripts
    │   ├── models/             # Model training and validation scripts
    │   └── api/                # API code for serving models
    │
    ├── tests/                  # Unit tests
    │
    ├── scripts/                # Utility scripts
    │
    ├── docker/                 # Docker configurations
    │
    ├── .gitignore              # Git ignore file
    ├── requirements.txt        # Python dependencies
    └── README.md               # Project documentation
```
### Create a Python virtual environment

1. Install python if it hasn't been done already
    from python.org

2. Install VSCode and python extension for VSCode
    from code.visualstudio.com

3. Create a python virtual environment
    either with ctrl+shift+P -> python : create new environment
    or with 
    ```sh
    python -m venv venv
4. Install and manage the required libraries

    downloading required libraries of the project:
    ```sh
    pip install -r requirements.txt
    ```
    freeze the libraries as of the environment
    ```sh
    pip freeze > requirements.txt
    ```

5. Activate the environment as the source
    ```sh
    source venv/bin/activate
### Version Control with Git

1. Initialize Git Repository
    ```sh
    git init
2. Create a .gitignore File
    Add common files and directories to ignore:
    ```python
    __pycache__/
    *.pyc
    .DS_Store
    .venv/
    data/
    models/
3. Commit Initial Structure
    ```bash
    git add .
    git commit -m "Initial project structure"
4. Push to a distant repo
    ```bash
   git push --set-upstream origin 'feature/your_distant_branch_name'
### Basic Git Commands

- **Create a new branch:**
    ```sh
    git checkout -b feature/your-feature-name
- **Commit changes:**
    ```sh
    git add .
    git commit -m "Add feature description"
- **Push changes:**
    ```sh 
    git push origin feature/your-feature-name
- **Merge changes:**
    - Open a pull request to merge your feature branch into dev or main.
    - Review and test before merging.
- **Pull Latest changes:**
    ```sh 
    git checkout dev
    git pull origin dev
### Data Versioning with DVC

- **Initialize DVC**
    ```sh 
    dvc init
- **Track data files**
    ```sh 
    dvc add data/raw/synthetic_data.csv
- **Commit dvc changes**
    ```sh 
    git add data/raw/synthetic_data.csv.dvc .dvc/config
    git commit -m "Track data with DVC"
##  Transforming Jupyter Notebooks

### Organize Code into Functions
1. Start from jupyter notebooks
2. Identify reusable code blocks in your botebooks
3. Convert them to functions and place them in appropriate modules under src/

- **Example Transformation**
    ```python
    from sklearn.datasets import make_classification
    import pandas as pd

    X, y = make_classification(n_samples=1000, n_features=20)
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    df['target'] = y
- **Transformed Code in src/data/synthetic.py**
    ```python
    from sklearn.datasets import make_classification
    import pandas as pd
    def generate_synthetic_data(n_samples=1000, n_features=20):
        """
        Generate synthetic classification data.

        Parameters:
        - n_samples: int, default=1000
            The number of samples.
        - n_features: int, default=20
            The number of features.

        Returns:
        - df: DataFrame
            A DataFrame containing the synthetic data with features and target.
        """
        X, y = make_classification(n_samples=n_samples, n_features=n_features)
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(n_features)])
        df['target'] = y
        return df
- **Document the process**
    Use comments and docstrings to explain the purpose of each function.
    Maintain a README file to guide users on how to run the project.

### Detailed Explanation of Key Python Files

- **src/data/synthetic.py**

    This file is responsible for generating synthetic data for model training and validation.
    
    - Key Components
        - SyntheticDataGenerator Class
        - Purpose: To encapsulate the logic for generating synthetic classification data.
        - Methods:
            - \_\_init__(self, n_samples=1000, n_features=20): Initializes the generator with the number of samples and features.
            - generate_data(self): Uses make_classification from scikit-learn to create synthetic data and returns it as a DataFrame.
            - save_data(self): Saves the generated data to a CSV file in the data/raw directory.
    - Example Usage
        ```python
        generator = SyntheticDataGenerator()
        generator.save_data()
- **src/models/train.py**

    This file handles the training of the machine learning model.
    - Key Components
        - train_model Function:
        - Purpose: To train a RandomForest model using the synthetic data.
        - Steps:
            - 1. Load the data from data/raw/synthetic_data.csv
            - 2. Split the data into features (X) and target (y)
            - 3. Initialize and train a RandomForestClassifier
            - 4. Save the trained model to models/model.joblib using joblib.
    - Example Usage
        ```python
        train_model()
- **src/models/validate.py**

    This file is responsible for validating the trained model.
    - Key Components
        - validate_model Function:
        - Purpose: To validate the trained model on the test data and calculate accuracy.
        - Steps:
            - 1. Load the trained model from models/model.joblib
            - 2. Load the test data from data/raw/synthetic_data.csv
            - 3. Make predictions using the model
            - 4. Calculate and return the accuracy score.
    - Example Usage
        ```python
        accuracy = validate_model()
        print(f"Validation accuracy: {accuracy:.4f}")
4. airflow/dags/training_dag.py
    This file defines the Airflow DAG for orchestrating the data generation, model training, and validation tasks.
    - Key Components
        - DAG Definition:
        - Purpose: To automate the workflow of generating data, training the model, and validating it.
        - Tasks:
            - generate_data_task: Calls the generate_data function to create synthetic data.
            - train_model_task: Calls the train function to train the model.
            - validate_model_task: Calls the validate function to validate the model.
            - Error Handling: Each task includes error handling to ensure that any issues are logged and raised appropriately.
    - Example Usage
        - The DAG is automatically triggered by Airflow based on the schedule defined in the DAG configuration.

# API Development

## FastAPI Overview

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Key Features

- Automatic Interactive API Documentation: FastAPI generates interactive API documentation using Swagger UI and ReDoc.
-  Data Validation: Uses Pydantic for data validation and settings management.
-  Asynchronous Support: Built on Starlette for asynchronous request handling.

## Example API structure

### src/api/main.py

This file defines the API endpoints for serving the machine learning model.
```python
    from fastapi import FastAPI
    import joblib
    import numpy as np
    app = FastAPI()
    # Load the trained model
    model = joblib.load("models/model.joblib")
    @app.get("/")
    def read_root():
        return {"message": "Welcome to the ML model API"}
    @app.post("/predict/")
    def predict(features: list):
        """Predict using the trained model"""
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)
        return {"prediction": prediction.tolist()}
```
## Key Endpoints

- Root Endpoint:
- Path: /
- Method: GET
- Description: Returns a welcome message.
- Prediction Endpoint:
- Path: /predict/
- Method: POST
- Description: Accepts a list of features and returns a prediction from the trained model.
- Example Request:
    ```python
     {
       "features": [0.1, 0.2, 0.3, ..., 0.9]
     }
## Running the API

- Start the API:
    ```sh
    uvicorn src.api.main:app --reload
- Access the API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redocThis setup provides a robust framework for developing, testing, and deploying machine learning models as APIs, ensuring consistency and scalability.


# Docker in MLOps Projects

## What We are Building

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

## What is Docker

Docker is like a shipping container for software. It packages everything your application needs to run (code, dependencies, settings) into a standardized unit called a container. This ensures that your application works the same way everywhere.



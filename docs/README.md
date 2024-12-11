# MLOps Project Setup Guide

## Introduction

This guide will walk you through transforming Jupyter notebooks into a structured MLOps project. We'll cover best practices, including setting up version control, organizing your code, and using tools like DVC for data versioning.

## Table of Contents

1. [Set Up the Environment](#set-up-the-environment)
    - [Project Structure](#project-structure)
    - [Create a Python Virtual Environment](#create-a-python-virtual-environment)
    - [Version Control with Git](#version-control-with-git)
    - [Data Versioning with DVC](#data-versioning-with-dvc)
2. [Transforming Jupyter Notebooks](#transforming-jupyter-notebooks)
    - [Organize Code into Functions](#organize-code-into-functions)
    - [Example Transformation](#example-transformation)
    - [Document the Process](#document-the-process)
3. [Detailed Explanation of Key Python Files](#detailed-explanation-of-key-python-files)
    - [`src/data/synthetic.py`](#srcdatasyntheticpy)
    - [`src/models/train.py`](#srcmodelstrainpy)
    - [`src/models/validate.py`](#srcmodelsvalidatepy)
    - [`airflow/dags/training_dag.py`](#airflowdagstraining_dagpy)
4. [Docker in MLOps Projects](#docker-in-mlops-projects)
   - [Introduction to Docker](#introduction-to-docker)
   - [Why Use Docker?](#why-use-docker)
   - [Docker in This Project](#docker-in-this-project)
   - [Controlling Training and DVC with Docker](#controlling-training-and-dvc-with-docker)
5. [Running the Project](#running-the-project)
6. [Conclusion](#conclusion)

## Set up the environment

### Project Structure

Get the project structure from the provided zip file
It should look like this:

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

### Create a Python virtual environment

1. Install python if it hasn't been done already
    from python.org

2. Install VSCode and python extension for VSCode
    from code.visualstudio.com

3. Create a python virtual environment
    either with python -m venv venv command
    or with ctrl+shift+P -> python : create new environment

4. Install and manage the required libraries
    pip install -r requirements.txt for downloading required libraries of the project
    pip freeze > requirements.txt to freeze the libraries as of the environment ones

5. Activate the environment as the source
    source venv/bin/activate

### Version Control with Git

1. Initialize Git Repository
    git init

2. Create a .gitignore File
    Add common files and directories to ignore:
    __pycache__/
    *.pyc
    .DS_Store
    .venv/
    data/
    models/

3. Commit Initial Structure
   git add .
   git commit -m "Initial project structure"

4. Push to a distant repo
   git push --set-upstream origin 'feature/your_distant_branch_name'

5. Basic git commands
### Basic Git Commands

- **Basic Git Commands**
  ```sh
    - Create a new branch:
      ```
      git checkout -b feature/your-feature-name
      ```
    - Commit Changes:
      ```
      git add .
      git commit -m "Add feature description"
      ```
    - Push Changes:
      ```
      git push origin feature/your-feature-name
      ```
    - Merge Changes:
      - Open a pull request to merge your feature branch into dev or main.
      - Review and test before merging.
    - Pull Latest Changes:
      ```
      git checkout dev
      git pull origin dev
      ```

### Data Versioning with DVC

1. Initialize DVC
   dvc init

2. Track Data Files
   dvc add data/raw/synthetic_data.csv

3. Commit DVC Changes
   git add data/raw/synthetic_data.csv.dvc .dvc/config
   git commit -m "Track data with DVC"

##  Transforming Jupyter Notebooks

### Organize Code into Functions
1. Start from jupyter notebooks
2. Identify reusable code blocks in your botebooks
3. Convert them to functions and place them in appropriate modules under src/

### Example Transformation:
    ```python
        from sklearn.datasets import make_classification
        import pandas as pd

        X, y = make_classification(n_samples=1000, n_features=20)
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
        df['target'] = y
        ```
    
    Transformed Code in src/data/synthetic.py

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
        ```

4. Document the process
    Use comments and docstrings to explain the purpose of each function.
    Maintain a README file to guide users on how to run the project.

### Detailed Explanation of Key Python Files

1. src/data/synthetic.py

    This file is responsible for generating synthetic data for model training and validation.
    
    Key Components
        •  SyntheticDataGenerator Class
        •  Purpose: To encapsulate the logic for generating synthetic classification data.
        •  Methods:
            •  __init__(self, n_samples=1000, n_features=20): Initializes the generator with the number of samples and features.
            •  generate_data(self): Uses make_classification from scikit-learn to create synthetic data and returns it as a DataFrame.
            •  save_data(self): Saves the generated data to a CSV file in the data/raw directory.
    Example Usage
        generator = SyntheticDataGenerator()
        generator.save_data()
2. src/models/train.py
    This file handles the training of the machine learning model.
    Key Components
        •  train_model Function:
        •  Purpose: To train a RandomForest model using the synthetic data.
        •  Steps:1. Load the data from data/raw/synthetic_data.csv.2. Split the data into features (X) and target (y).3. Initialize and train a RandomForestClassifier.4. Save the trained model to models/model.joblib using joblib.
    Example Usage
        train_model()
3. src/models/validate.py
    This file is responsible for validating the trained model.
    Key Components
        •  validate_model Function:
        •  Purpose: To validate the trained model on the test data and calculate accuracy.
        •  Steps:1. Load the trained model from models/model.joblib.2. Load the test data from data/raw/synthetic_data.csv.3. Make predictions using the model.4. Calculate and return the accuracy score.
    Example Usage
        accuracy = validate_model()
        print(f"Validation accuracy: {accuracy:.4f}")
4. airflow/dags/training_dag.py
    This file defines the Airflow DAG for orchestrating the data generation, model training, and validation tasks.
    Key Components
        •  DAG Definition:
        •  Purpose: To automate the workflow of generating data, training the model, and validating it.
        •  Tasks:
            •  generate_data_task: Calls the generate_data function to create synthetic data.
            •  train_model_task: Calls the train function to train the model.
            •  validate_model_task: Calls the validate function to validate the model.
            •  Error Handling: Each task includes error handling to ensure that any issues are logged and raised appropriately.
    Example Usage
        The DAG is automatically triggered by Airflow based on the schedule defined in the DAG configuration.


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



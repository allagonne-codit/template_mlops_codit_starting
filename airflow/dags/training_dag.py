from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import os
import sys

# Define base paths relative to mounted volumes in docker-compose
BASE_PATH = '/opt/airflow'
DATA_PATH = os.path.join(BASE_PATH, 'data/raw')
MODEL_PATH = os.path.join(BASE_PATH, 'models')

def generate_data(**context):
    """Generate synthetic data"""
    try:
        # Debug information
        print("Current working directory:", os.getcwd())
        print("Python path:", sys.path)
        print("Directory contents:", os.listdir('/app/src'))
        
        # Add src to Python path
        if '/app' not in sys.path:
            sys.path.append('/app')
        
        from src.data.synthetic import SyntheticDataGenerator
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_PATH, exist_ok=True)
        
        # Generate and save data
        generator = SyntheticDataGenerator()
        data_file = os.path.join(DATA_PATH, 'synthetic_data.csv')
        generator.save_data(data_file)
        
        print(f"Data generated successfully and saved to {data_file}")
        return "Data generated successfully"
    except ImportError as e:
        print(f"Import Error: {str(e)}")
        print("Python path:", sys.path)
        raise
    except Exception as e:
        print(f"Error in generate_data: {str(e)}")
        raise

def train(**context):
    """Train the model"""
    try:
        from src.models.train import train_model
        
        # Create model directory if it doesn't exist
        os.makedirs(MODEL_PATH, exist_ok=True)
        
        # Set MLflow tracking URI
        mlflow.set_tracking_uri("http://mlflow:5000")
        
        # Train model
        data_file = os.path.join(DATA_PATH, 'synthetic_data.csv')
        model_file = os.path.join(MODEL_PATH, 'model.pkl')
        
        print(f"Training model with data from {data_file}")
        train_model(
            data_path=data_file,
            model_path=model_file
        )
        print(f"Model saved to {model_file}")
        return "Model trained successfully"
    except Exception as e:
        print(f"Error in train: {str(e)}")
        raise

def validate(**context):
    """Validate the model"""
    try:
        from src.models.validate import validate_model
        
        data_file = os.path.join(DATA_PATH, 'synthetic_data.csv')
        model_file = os.path.join(MODEL_PATH, 'model.pkl')
        
        print(f"Validating model {model_file} with data from {data_file}")
        accuracy = validate_model(
            data_path=data_file,
            model_path=model_file
        )
        print(f"Model validation accuracy: {accuracy}")
        return f"Model validated with accuracy: {accuracy}"
    except Exception as e:
        print(f"Error in validate: {str(e)}")
        raise

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,  # Increased retries
    'retry_delay': timedelta(minutes=1),  # Shorter retry delay for testing
    'catchup': False,
}

dag = DAG(
    'model_training_pipeline',
    default_args=default_args,
    description='A pipeline to train and validate ML model',
    schedule=timedelta(days=1),
    catchup=False
)

# Tasks
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    provide_context=True,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train,
    provide_context=True,
    dag=dag
)

validate_model_task = PythonOperator(
    task_id='validate_model',
    python_callable=validate,
    provide_context=True,
    dag=dag
)

# Set dependencies
generate_data_task >> train_model_task >> validate_model_task
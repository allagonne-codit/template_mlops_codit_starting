from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import os

# Add the project root to Python path
import sys
sys.path.append('/opt/airflow/dags')
sys.path.append('/app')  # This is where our source code is mounted in the container

from src.data.synthetic import SyntheticDataGenerator
from src.models.train import train_model
from src.models.validate import validate_model

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'model_training_pipeline',
    default_args=default_args,
    description='ML model training pipeline',
    schedule=timedelta(days=1),
    catchup=False
)

def generate_data(**context):
    """Generate synthetic data"""
    try:
        # Change to the correct working directory
        os.chdir('/app')
        
        generator = SyntheticDataGenerator()
        generator.save_data()
        
        # Verify the file was created
        if not os.path.exists('data/raw/synthetic_data.csv'):
            raise FileNotFoundError("Data file was not created successfully")
            
    except Exception as e:
        print(f"Error in generate_data: {str(e)}")
        raise

def train(**context):
    """Train the model"""
    try:
        # Change to the correct working directory
        os.chdir('/app')
        
        mlflow.set_tracking_uri("http://mlflow:5000")
        train_model()
        
        # Verify the model was created
        if not os.path.exists('models/model.joblib'):
            raise FileNotFoundError("Model file was not created successfully")
            
    except Exception as e:
        print(f"Error in train: {str(e)}")
        raise

def validate(**context):
    """Validate the model"""
    try:
        # Change to the correct working directory
        os.chdir('/app')
        
        accuracy = validate_model()
        print(f"Model validation accuracy: {accuracy}")
        
    except Exception as e:
        print(f"Error in validate: {str(e)}")
        raise

# Define tasks
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

# Set task dependencies
generate_data_task >> train_model_task >> validate_model_task
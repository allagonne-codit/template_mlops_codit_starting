from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import os

# Define base paths
APP_PATH = '/app'
DATA_PATH = os.path.join(APP_PATH, 'data/raw')
MODEL_PATH = os.path.join(APP_PATH, 'models')

# Ensure directories exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)

def generate_data(**context):
    """Generate synthetic data"""
    from src.data.synthetic import SyntheticDataGenerator
    
    generator = SyntheticDataGenerator()
    generator.save_data(os.path.join(DATA_PATH, 'synthetic_data.csv'))
    return "Data generated successfully"

def train(**context):
    """Train the model"""
    from src.models.train import train_model
    
    mlflow.set_tracking_uri("http://mlflow:5000")
    train_model(
        data_path=os.path.join(DATA_PATH, 'synthetic_data.csv'),
        model_path=os.path.join(MODEL_PATH, 'model.joblib')
    )
    return "Model trained successfully"

def validate(**context):
    """Validate the model"""
    from src.models.validate import validate_model
    
    accuracy = validate_model(
        data_path=os.path.join(DATA_PATH, 'synthetic_data.csv'),
        model_path=os.path.join(MODEL_PATH, 'model.joblib')
    )
    print(f"Model validation accuracy: {accuracy}")
    return f"Model validated with accuracy: {accuracy}"

# DAG definition
dag = DAG(
    'model_training_pipeline',
    default_args={
        'owner': 'mlops',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    schedule=timedelta(days=1),
    catchup=False
)

# Tasks
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train,
    dag=dag
)

validate_model_task = PythonOperator(
    task_id='validate_model',
    python_callable=validate,
    dag=dag
)

# Set dependencies
generate_data_task >> train_model_task >> validate_model_task
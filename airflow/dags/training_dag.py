from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

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
    schedule_interval=timedelta(days=1),
    catchup=False
)

def generate_data():
    generator = SyntheticDataGenerator()
    generator.save_data()

def train():
    with mlflow.start_run():
        train_model()

def validate():
    validate_model()

# Define tasks
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

# Set task dependencies
generate_data_task >> train_model_task >> validate_model_task
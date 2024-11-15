import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
import sklearn
import socket

def train_model(data_path: str, model_path: str):
    """Train the model and log metrics with MLflow"""
    # Set MLflow tracking URI based on environment
    # Check if mlflow host is available (running in Docker)
    try:
        socket.gethostbyname('mlflow')
        mlflow.set_tracking_uri("http://mlflow:5000")
    except socket.gaierror:
        # Running locally - either skip MLflow or use local URI
        print("MLflow server not found - training without MLflow tracking")
        use_mlflow = False
    else:
        use_mlflow = True
    
    # Load data
    df = pd.read_csv(data_path)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    
    # Train model
    if use_mlflow:
        # Set up MLflow experiment
        experiment_name = "synthetic-classification"
        try:
            experiment_id = mlflow.create_experiment(experiment_name)
        except:
            experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        mlflow.set_experiment(experiment_name)
        
        with mlflow.start_run(experiment_id=experiment_id):
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Log parameters and metrics
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("model_type", "RandomForestClassifier")
            mlflow.log_param("sklearn_version", sklearn.__version__)
            mlflow.log_metric("accuracy", accuracy)
            
            # Save model using MLflow
            mlflow.sklearn.log_model(
                model, 
                "random_forest_model",
                registered_model_name="synthetic_classifier"
            )
    else:
        # Train without MLflow tracking
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
    
    # Save model locally using pickle
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")
    return accuracy

if __name__ == "__main__":
    accuracy = train_model(
        data_path='data/raw/synthetic_data.csv',
        model_path='models/model.pkl'
    )
    print(f"Model trained successfully! Accuracy: {accuracy:.4f}")
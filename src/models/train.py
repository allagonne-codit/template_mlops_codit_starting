import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def load_data():
    """Load the training data"""
    df = pd.read_csv('data/raw/synthetic_data.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model():
    """Train the model and log metrics with MLflow"""
    X_train, X_test, y_train, y_test = load_data()
    
    # Initialize model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.joblib')
    mlflow.sklearn.log_model(model, "random_forest_model")
    
    return accuracy

if __name__ == "__main__":
    accuracy = train_model()
    print(f"Model trained successfully! Accuracy: {accuracy:.2f}") 
import pandas as pd
from sklearn.metrics import accuracy_score
import joblib
import os

def validate_model():
    """Validate the trained model on test data"""
    # Load the model
    model_path = 'models/model.joblib'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    model = joblib.load(model_path)
    
    # Load test data
    data_path = 'data/raw/synthetic_data.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    df = pd.read_csv(data_path)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    
    return accuracy

if __name__ == "__main__":
    accuracy = validate_model()
    print(f"Validation completed successfully! Accuracy: {accuracy:.4f}") 
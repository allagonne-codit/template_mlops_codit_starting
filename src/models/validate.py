import pandas as pd
from sklearn.metrics import accuracy_score
import pickle
import os

def validate_model(data_path: str, model_path: str) -> float:
    """Validate the trained model on test data"""
    # Load the model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Load test data
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    df = pd.read_csv(data_path)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    print(f"Model validation accuracy: {accuracy:.4f}")
    
    return accuracy

if __name__ == "__main__":
    accuracy = validate_model(
        data_path='data/raw/synthetic_data.csv',
        model_path='models/model.pkl'
    )
    print(f"Validation completed successfully! Accuracy: {accuracy:.4f}") 
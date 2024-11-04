import pandas as pd
import joblib
from sklearn.metrics import classification_report
import json
import os

def validate_model():
    """Validate the trained model on test data"""
    # Load test data
    df = pd.read_csv('data/raw/synthetic_data.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Load model
    model = joblib.load('models/model.joblib')
    
    # Make predictions
    predictions = model.predict(X)
    
    # Generate validation report
    report = classification_report(y, predictions, output_dict=True)
    
    # Save validation results
    os.makedirs('reports', exist_ok=True)
    with open('reports/validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

if __name__ == "__main__":
    report = validate_model()
    print("Validation completed successfully!") 
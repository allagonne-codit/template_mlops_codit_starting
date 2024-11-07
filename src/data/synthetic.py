import numpy as np
from sklearn.datasets import make_classification
import pandas as pd
import os

class SyntheticDataGenerator:
    def __init__(self, n_samples=1000, n_features=20):
        self.n_samples = n_samples
        self.n_features = n_features
        
    def generate_data(self):
        """Generate synthetic classification data"""
        X, y = make_classification(
            n_samples=self.n_samples,
            n_features=self.n_features,
            n_informative=15,
            n_redundant=5,
            random_state=42
        )
        
        # Convert to DataFrame
        feature_names = [f'feature_{i}' for i in range(self.n_features)]
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        
        return df
    
    def save_data(self):
        """Generate and save data to CSV"""
        df = self.generate_data()
        
        # Create data directory if it doesn't exist
        os.makedirs('data/raw', exist_ok=True)
        
        # Save to CSV
        df.to_csv('data/raw/synthetic_data.csv', index=False)
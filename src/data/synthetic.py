import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
import os
import json
from datetime import datetime
from typing import Dict, Any

class SyntheticDataGenerator:
    def __init__(self, n_samples: int = 1000, n_features: int = 20):
        """
        Initialize the synthetic data generator.
        
        Args:
            n_samples: Number of samples to generate
            n_features: Number of features to generate
        """
        self.n_samples = n_samples
        self.n_features = n_features
        
    def generate_data(self) -> pd.DataFrame:
        """
        Generate synthetic classification dataset.
        
        Returns:
            DataFrame containing synthetic data
        """
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
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Generate metadata for the dataset.
        
        Returns:
            Dictionary containing dataset metadata
        """
        return {
            'n_samples': self.n_samples,
            'n_features': self.n_features,
            'creation_date': datetime.now().isoformat(),
            'feature_names': [f'feature_{i}' for i in range(self.n_features)],
            'target_type': 'binary_classification'
        }
    
    def save_data(self, output_dir: str = 'data/raw') -> None:
        """
        Save synthetic data and metadata to files.
        
        Args:
            output_dir: Directory to save the data
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save data
        df = self.generate_data()
        df.to_csv(os.path.join(output_dir, 'synthetic_data.csv'), index=False)
        
        # Save metadata
        metadata = self.get_metadata()
        with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Data saved successfully to {output_dir}")
        print(f"Generated {self.n_samples} samples with {self.n_features} features")

if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    generator.save_data()
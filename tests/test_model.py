import pandas as pd
import numpy as np
from src.models.train import train_model
from src.data.synthetic import SyntheticDataGenerator

def test_synthetic_data_generation():
    generator = SyntheticDataGenerator(n_samples=100)
    df = generator.generate_data()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert 'target' in df.columns

def test_model_training():
    # Generate test data
    generator = SyntheticDataGenerator(n_samples=100)
    generator.save_data()
    
    # Train model
    accuracy = train_model()
    
    assert isinstance(accuracy, float)
    assert 0 <= accuracy <= 1

def test_model_predictions():
    import joblib
    
    # Load model
    model = joblib.load('models/model.joblib')
    
    # Create sample input
    sample_input = np.random.rand(1, 20)
    
    # Make prediction
    prediction = model.predict(sample_input)
    
    assert prediction.shape == (1,)
    assert prediction[0] in [0, 1] 
    
test_model_predictions()
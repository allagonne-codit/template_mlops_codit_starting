from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from typing import List
import os
import logging

app = FastAPI(title="MLOps Demo API")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model at startup
MODEL_PATH = '/app/models/model.pkl'

def load_model():
    logger.info(f"Attempting to load model from {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file not found at {MODEL_PATH}")
        models_dir = os.path.dirname(MODEL_PATH)
        if os.path.exists(models_dir):
            logger.info(f"Contents of {models_dir}: {os.listdir(models_dir)}")
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Successfully loaded model of type {type(model)}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

model = None

try:
    model = load_model()
except Exception as e:
    logger.warning(f"Initial model load failed: {str(e)}")

class PredictionInput(BaseModel):
    features: List[float]

class PredictionOutput(BaseModel):
    prediction: int
    probability: float

@app.get("/health")
def health_check():
    global model
    if model is None:
        try:
            model = load_model()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Model not loaded: {str(e)}")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    global model
    if model is None:
        try:
            model = load_model()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Model not loaded: {str(e)}")
    
    try:
        if len(input_data.features) != 20:  # Adjust based on your model
            raise HTTPException(
                status_code=400, 
                detail=f"Expected 20 features, got {len(input_data.features)}"
            )
        
        features = np.array(input_data.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = float(model.predict_proba(features).max())
        
        return PredictionOutput(
            prediction=int(prediction),
            probability=probability
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
def model_info():
    global model
    if model is None:
        try:
            model = load_model()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Model not loaded: {str(e)}")
    
    return {
        "model_type": type(model).__name__,
        "feature_count": model.n_features_in_,
        "parameters": model.get_params()
    } 
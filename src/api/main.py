from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import mlflow.pyfunc

app = FastAPI(title="MLOps Demo API")

# Load the model at startup
model = joblib.load('models/model.joblib')

class PredictionInput(BaseModel):
    features: List[float]

class PredictionOutput(BaseModel):
    prediction: int
    probability: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    try:
        features = np.array(input_data.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features).max()
        
        return PredictionOutput(
            prediction=int(prediction),
            probability=float(probability)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
def model_info():
    return {
        "model_type": type(model).__name__,
        "feature_count": model.n_features_in_,
        "parameters": model.get_params()
    } 
# this is a FastAPI app (single file API). 
# It loads the saved pipeline and the metadata. It creates two end points: 
    # POST /predict — returns predicted LTV_12m 
    # POST /predict_batch — accept list of records


from fastapi import FastAPI, HTTPException                
from pydantic import BaseModel, Field                  
from typing import List                                                                                                                                              
import joblib                 
import json                   
import numpy as np                 
import pandas as pd                  
from pathlib import Path                 

MODEL_PATH = Path("models/model.joblib") 
META_PATH = Path("models/feature_meta.json") 

app = FastAPI(title="LTV Predictor API") 
                                        
# Request schema for single prediction 
class PredictRequest(BaseModel): 
    
    cohort_month_str: str = Field(..., example="2017-01")    
    customer_state: str = Field(..., example="SP") 
    rev_1m: float = Field(..., ge=0.0)                 
    n_orders_1m: int = Field(..., ge=0)                 
    rev_3m: float = Field(..., ge=0.0)                 
    n_orders_3m: int = Field(..., ge=0) 

class PredictResponse(BaseModel): 
    ltv_12m_pred: float 
    
# Batch request 
class PredictBatchRequest(BaseModel):
    records: List[PredictRequest] 

def inv_log1p(y_log): 
    return np.expm1(y_log) 

    
    
# Load model + metadata on startup 
if not MODEL_PATH.exists(): 
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run save_model.py first.") 
    
model = joblib.load(MODEL_PATH) 
with open(META_PATH, "r") as f: 
    meta = json.load(f) 
    
feature_cols = meta["feature_cols"] 

# returns predicted LTV_12m 
@app.post("/predict", response_model=PredictResponse) 
def predict(req: PredictRequest): 
    row = {
        "cohort_month_str": req.cohort_month_str,                 
        "customer_state": req.customer_state,                  
        "rev_1m": req.rev_1m,                  
        "n_orders_1m": req.n_orders_1m,                  
        "rev_3m": req.rev_3m,                  
        "n_orders_3m": req.n_orders_3m, 
    }
    df = pd.DataFrame([row])[feature_cols] 
    try:
        y_log = model.predict(df)
        y = inv_log1p(y_log) 
        return {"ltv_12m_pred": float(y[0])} 
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e)) 

# accepts list of records
@app.post("/predict_batch") 
def predict_batch(req: PredictBatchRequest): 
    df = pd.DataFrame([r.dict() for r in req.records])[feature_cols]  
    try: 
        y_log = model.predict(df) 
        y = inv_log1p(y_log) 
        return {"predictions": [float(x) for x in y.tolist()]} 
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))  

        
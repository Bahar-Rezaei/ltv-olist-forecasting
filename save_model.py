# save_model.py reproduces the training pipeline used in the notebook (same ColumnTransformer, encoder, column order), fits it on the training data, and saves the artifact plus a small metadata file with feature column order.                                                                                                                                                                    
import pandas as pd                 
import numpy as np                  
                
# ---------- LOAD DATA----------                                                                                                            

data_dir = "./data"
model_df = pd.read_csv(f"{data_dir}/model_df.csv", parse_dates=["first_order_date"])                   
                                                                                          
# ---------- FEATURES & TARGET (must match inference order) ----------                                                                                
feature_cols = [                                                                                                                 
    "cohort_month_str",                                                                                                          
    "customer_state",                                                                                                            
    "rev_1m",                                                                                                                    
    "n_orders_1m",                                                                                                               
    "rev_3m",                                                                                                                    
    "n_orders_3m",                                                                                                               
]                                                                                                                                
target_col = "ltv_12m"                 
                       
# Train/test split by time (same as notebook)  
cutoff_date = pd.to_datetime("2017-12-31")                                                                                                           
train_df = model_df[model_df["first_order_date"] <= cutoff_date].copy()                 
                                                                        
X_train = train_df[feature_cols]                                                                                              
y_train = train_df[target_col]                 
                                                                                                                                                                      
# log1p transform target for training stability 
y_train_log = np.log1p(y_train) 

                                
# ---------- PREPROCESS + MODEL ----------    

from sklearn.preprocessing import OneHotEncoder                 
from sklearn.compose import ColumnTransformer                 
from sklearn.pipeline import Pipeline                 
from sklearn.ensemble import GradientBoostingRegressor 

cat_cols = ["cohort_month_str", "customer_state"]                 
num_cols = ["rev_1m", "n_orders_1m", "rev_3m", "n_orders_3m"] 
                                                              
preprocess = ColumnTransformer(                                                                                                  
    transformers=[                                                                                                               
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),                                                               
        ("num", "passthrough", num_cols),                                                                                        
    ]                                                                                                                            
) 

model = GradientBoostingRegressor(random_state=42)                  

pipe = Pipeline(                 
    steps=[                 
        ("preprocess", preprocess),                 
        ("model", model),                 
    ]                 
) 

pipe.fit(X_train, y_train_log) 


# ---------- SAVE MODEL + METADATA ----------    

import joblib                
import json  
import os

os.makedirs("./models", exist_ok=True)
joblib.dump(pipe, "models/model.joblib")

meta = {                 
    "feature_cols": feature_cols,                 
    "cat_cols": cat_cols,                 
    "num_cols": num_cols,                 
    "target": target_col,                 
    "note": "Model trained with log1p(target) transformation. Use inv: expm1."                 
} 
with open("models/feature_meta.json", "w") as f:                 
    json.dump(meta, f) 

print("Saved models/model.joblib and models/feature_meta.json") 


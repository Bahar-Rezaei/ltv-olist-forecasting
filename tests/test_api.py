
# test: uses FastAPI TestClient to ensure endpoint runs.

from fastapi.testclient import TestClient   
from app.main import app

client = TestClient(app)           
                         
def test_predict_single():                 
     payload = {"cohort_month_str": "2017-01",                  
         "customer_state": "SP",                  
         "rev_1m": 10.0,                  
         "n_orders_1m": 1,                  
         "rev_3m": 10.0,                  
         "n_orders_3m": 1                  
     }                  
     r = client.post("/predict", json=payload) 
     assert r.status_code == 200 
     data = r.json() 
     assert "ltv_12m_pred" in data 
     assert data["ltv_12m_pred"] >= 0 
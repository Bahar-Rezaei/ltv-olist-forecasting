# Customer LTV & Cohort Forecasting — Olist case study   

This is a compact, actionable analysis and ML pipeline that estimates 12‑month customer lifetime value ($LTV_{12m}$) for an       
e‑commerce marketplace using the public Olist dataset. It’s built to be interview- and recruiter-friendly: clear business    
question, reproducible steps, one baseline model, and practical recommendations a product or marketing team can act on.  

---

## What this project does (one sentence)?

Compute cohort revenue and retention, build $LTV_{12m}$ labels, train a simple predictive model using the first 1–3 months of     
customer behaviour, and show business‑facing metrics (MAE, decile evaluation, revenue capture).  

---

## Why this matters?                                                       

If you run acquisition or CRM, you need to know:                                                                             

- How much a new customer is worth over 12 months.                                                                          
- Which cohorts/regions/categories bring the best customers.                                                                
- When to invest in onboarding and retention to get the most return.                                                        

This project shows how to answer those questions with data and turn the answers into practical actions.  

---

## Data 

Source: Olist Brazilian e‑commerce dataset on Kaggle.                                                                        
[Olist dataset main page] (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).                                       

Required (place in **data/**):                                                                                                   

- **olist_orders_dataset.csv** 
- **olist_order_payments_dataset.csv** 
- **olist_customers_dataset.csv** 

Optional (better segmentation if present):                                                                                   

- olist_order_items_dataset.csv, olist_products_dataset.csv, olist_sellers_dataset.csv, olist_order_reviews_dataset.csv     

(Repository does not include the raw CSVs.)   

---

## Core pipeline (short)                                                    

1. Filter delivered orders and compute order revenue (sum of payments).                                                      
2. Build customer summary: first purchase date, cohort_month, n_orders, total_revenue.                                       
3. Define t_months = months since first order; compute cohort revenue per original cohort customer and retention rates.      
4. Label: $LTV_{12m}$ = sum(order_revenue) for months $0, ..., 11$.                                                                      
5. Features: cohort_month, customer_state, rev_1m, n_orders_1m, rev_3m, n_orders_3m.                                         
6. Baseline model: GradientBoostingRegressor on $log1p(LTV_{12m})$.                                                               
7. Business metrics: MAE/RMSE on original scale, decile MAE, and revenue capture by top predicted deciles.

---

## Key results (TL;DR)                                                     

- Revenue is front‑loaded: most $LTV$ accrues in months 0–6 (extended to 12 months for completeness).                         
- Retention drops fast after the first month; a small repeat cohort drives long‑run revenue.                                
- $LTV_{12m}$ is heavy‑tailed (median around 100s; a few whales skew the mean).                                                  
- Baseline model: low MAE (~ a few currency units ≈ $3–4\%$ of median $LTV$) and useful ranking power — the top predicted $10\%$     
   capture a substantial share of realized revenue (see notebook for exact number).                                         

---

## Practical recommendations                                                  

- Focus onboarding on converting first‑time buyers into a second purchase within 30–60 days (emails, personalised bundles,  
   category nudges).                                                                                                         
- Bid CAC and allocate channels by predicted LTV instead of a single average.                                               
- Use predicted LTV to target experiments and CRM flows (test richer experiences for high‑predicted‑LTV users).             

---

## What’s in the repo                                                      

- **notebooks/ltv_olist_analysis.ipynb** — full analysis (EDA, cohort tables, modeling).                                        
- **notebooks/ltv_demo.ipynb** — short, runnable demo for reviewers (small sample + lightweight model).                         
- **data/** — place raw CSVs here (not included).                                                                               
- **models/** — saved model artifact (models/model.joblib) if present.                                                          
- **app/** — FastAPI prediction endpoint (optional).                                                                            
- **tests/** — minimal unit tests.                                                                                              
- **Dockerfile**, **requirements.txt**, **README.md**.                                                                                  

---

## Quick start (run locally)                                                  

1. Create and activate a Python environment (venv or conda). Example:  
```
python -m venv venv 
source venv/bin/activate   # macOS / Linux
```

2. Install dependencies:
```
pip install -r requirements.txt
```
3. Download Olist CSVs from Kaggle and put required files in **data/**.

4. For a fast review, open **notebooks/ltv_demo.ipynb** — it uses a small preprocessed sample and either trains a quick model or
   loads **models/model_demo.joblib** if present.

5. To run the API (if **models/model.joblib** exists):
```
uvicorn app.main:app --reload --port 8000
```

   Example request: 
```
curl -X POST "http://localhost:8000/predict" \
      -H "Content-Type: application/json" \
      -d '{"cohort_month_str":"2017-01","customer_state":"SP","rev_1m":10,"n_orders_1m":1,"rev_3m":10,"n_orders_3m":1}' 
```                                                                                                                         

---

 ## Reproducibility notes                                                    

- The notebook writes **data/model_df.csv** (one row per customer) so the modeling and API scripts can run without reprocessing 
   raw tables.                                                                                                               
- For demo convenience, include **data/model_df_demo.csv** (small sample) and a prebuilt models/model_demo.joblib so reviewers  
   can run the demo in <5 minutes.                                                                                           

---

## Next improvements

- Use strict time‑based train/test splits for deployment realism.                                                           
- Add product/seller features, inter‑purchase timing, and richer models (XGBoost / LightGBM).                               
- Report business metrics (decile MAE, revenue capture, CAC payback) and embed the model in a small dashboard or API for    
   stakeholders.                                                                                                             





   

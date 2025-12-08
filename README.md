# Customer LTV & Cohort Forecasting for an E‑commerce Marketplace (Olist)

## Goal                                                                                                                          
                                                                                                                                  
This project builds a **lifetime value (LTV)** and **cohort‑based demand forecasting** analysis for an e‑commerce marketplace,   
using the Olist Brazilian e‑commerce dataset from Kaggle.                                                                        
                                                                                                                                  
We:                                                                                                                              
                                                                                                                                  
- Define customer cohorts by first purchase month.                                                                               
- Analyse **revenue per customer and retention over time** (cohort and retention heatmaps).                                      
- Construct a **12‑month LTV (LTV_12m)** per customer.                                                                           
- Build a simple **LTV_12m prediction model** using early behaviour features.                                                    
- Derive **marketing and product recommendations** based on the results.                                                         
                                                                                                                                 
## Data                                                                                                                          
                                                                                                                                 
The data comes from the public Olist Brazilian E‑Commerce dataset on Kaggle:                                                     
                                                                                                                                 
- Olist main page: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce                                                   
                                                                                                                                  
Due to licensing and file size, the raw CSV files are **not** included in this repository.                                       
                                                                                                                                  
To run the notebook:                                                                                                             
                                                                                                                                  
1. Download the dataset from Kaggle.                                                                                             
2. Place the following CSV files into a local `data/` folder:                                                                    
   - `olist_orders_dataset.csv`                                                                                                  
   - `olist_order_payments_dataset.csv`                                                                                          
   - `olist_customers_dataset.csv`                                                                                               
                                                                                                                                 
You may keep additional tables (order items, products, reviews, etc.) in `data/` if you want to extend the analysis.             
                                                                                                                                  
## Methods                                                                                                                       
                                                                                                                                  
1. **Order and customer tables**                                                                                                 
                                                                                                                                  
   - Filter to delivered orders.                                                                                                 
   - Aggregate `order_payments` to get **order_revenue** per `order_id`.                                                         
   - Join orders with customers to obtain `customer_unique_id` and `customer_state`.                                             
   - Build a customer‑level table:                                                                                               
     - `first_order_date`, `cohort_month`, `n_orders`, `total_revenue`.                                                          
                                                                                                                                  
2. **Cohort and retention analysis**                                                                                             
                                                                                                                                 
   - Define **cohorts** by `cohort_month = first_order_date.to_period("M")`.                                                     
   - Compute `t_months` = months since first order for each order.                                                               
   - For each `cohort_month` × `t_months`, compute:                                                                              
     - total revenue,                                                                                                            
     - revenue per original cohort customer,                                                                                     
     - retention rate (fraction of customers with ≥1 order by `t_months`).                                                       
   - Visualize:                                                                                                                  
     - cohort revenue heatmap,                                                                                                   
     - cumulative LTV per customer heatmap,                                                                                      
     - retention heatmap.                                                                                                        
                                                                                                                                 
3. **LTV_12m modeling**                                                                                                          
                                                                                                                                 
   - Define **LTV_12m** as total revenue in the first 12 months after first order (`t_months ∈ [0, 11]`).                        
   - Engineer early‑behaviour features per customer:                                                                             
     - `rev_1m`, `n_orders_1m` (first month),                                                                                    
     - `rev_3m`, `n_orders_3m` (first 3 months).                                                                                 
   - Fit a Gradient Boosting Regressor on `log(LTV_12m + 1)` using:                                                              
     - cohort month, customer state, and early‑behaviour features.                                                               
   - Evaluate on a held‑out test set using MAE and RMSE.                                                                         
                                                                                                                                  
## Results & Insights (Summary)                                                                                                  
                                                                                                                                  
- **Cohort revenue and LTV curves**                                                                                              
  Revenue per customer is heavily **front‑loaded**: most cohorts realise the bulk of their LTV within the first 6–12 months. Aft 
that, incremental gains are small.                                                                                               
                                                                                                                                  
- **Retention patterns**                                                                                                         
  Retention drops sharply after the first few months, with many one‑time buyers and a smaller base of repeat customers, which is 
typical for e‑commerce.                                                                                                          
                                                                                                                                  
- **LTV_12m distribution**                                                                                                       
  Among ~93k customers, median LTV_12m is about 108, mean is ~165, and maximum is >13,600, indicating a strongly skewed          
 distribution with a small number of “whales”.                                                                                    
                                                                                                                                  
 - **LTV_12m model performance**                                                                                                  
   The baseline Gradient Boosting model using early‑behaviour features achieves:                                                  
   - MAE ≈ 3.7                                                                                                                    
   - RMSE ≈ 59.3                                                                                                                  
   Relative to a median LTV_12m of ~108, the MAE is only about 3–4% of a typical customer’s LTV, indicating very accurate         
 predictions for most customers. The higher RMSE is driven by a few very high‑LTV outliers.                                       
                                                                                                                                  
 ## Business Recommendations (Brief)                                                                                              
                                                                                                                                  
 1. **Prioritise early‑life engagement**                                                                                          
    Since early behaviour strongly predicts LTV_12m and most value is realised in the first 6–12 months, onboarding and early‑lif 
 campaigns (e.g. incentives for a second order in the first 30–60 days) should be a key focus.                                    
                                                                                                                                  
 2. **Allocate acquisition budget by cohort quality**                                                                             
    Differences in cohort‑level LTV suggest that some acquisition periods or segments bring in more valuable customers. Acquisiti 
 budget should be biased towards those high‑LTV cohorts, with CAC targets proportional to expected LTV.                           
                                                                                                                                  
 3. **Use LTV predictions in retention & CRM**                                                                                    
    Integrating LTV_12m predictions into CRM systems enables early identification of high‑value customers, avoids over‑spending o 
 low‑value segments, and allows tracking of how changes to onboarding and UX affect long‑term value.                              
                                                                                                                                  
 ## Repository Structure                                                                                                          
                                                                                                                                  
 - `notebooks/ltv_olist_analysis.ipynb` – main analysis notebook (EDA, cohorts, LTV, modeling).                                   
 - `data/` – folder for raw CSV files (not tracked in git).                                                                       
 - `README.md` – project overview, methods, and results.                                                                          
 - `requirements.txt` – Python dependencies.                                                                                      
                                                                                                                                  
 ## How to Run                                                                                                                    
                                                                                                                                  
 1. Create and activate a Python environment (e.g. using `venv` or `conda`).                                                      
 2. Install dependencies:                                                                                                         
                                                                                                                                  
    ```bash                                                                                                                       
    pip install -r requirements.txt                                                                                               
                                                                                                                                  

 3 Download the Olist dataset from Kaggle and place the required CSV files into data/.                                            
 4 Open notebooks/ltv_olist_analysis.ipynb in Jupyter or VS Code and run all cells. EOF 


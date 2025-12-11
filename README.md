# Customer LTV & Cohort Forecasting for an E‑commerce / Marketplace Platform (Olist)

## Overview

This project builds an end‑to‑end analytics and ML workflow for an e‑commerce marketplace, inspired by platforms such as          
Booking.com or bol.com.                                                                                                 

Using the public Olist Brazilian e‑commerce dataset, it:                                                                          

 • Performs cohort‑based revenue and retention analysis.                                                                          
 • Constructs 12‑month customer lifetime value (LTV₁₂ₘ) labels.                                                                   
 • Trains a predictive model of LTV₁₂ₘ from early customer behaviour.                                                             
 • Derives concrete marketing and product recommendations for acquisition and retention.                                          

The project demonstrates how a product‑oriented data scientist can connect exploratory analysis, modeling, and business decisions 
in a marketplace context.  

## Business Goal                                                                                                                          
                                                                                                                                  
Marketplaces and e‑commerce platforms need to answer questions such as:                                                           

 • How much is a new customer likely to be worth over the next 12 months?                                                         
 • Which cohorts (time periods, geographies, segments) bring high‑quality customers?                                              
 • When in the customer lifecycle is most value realised, and how does retention evolve over time?                                

This project addresses these questions by:                                                                                        

 • Defining cohorts by first purchase month.                                                                                      
 • Measuring revenue and retention over time by cohort.                                                                           
 • Predicting 12‑month LTV from the first 1–3 months of behaviour.                                                                
 • Translating insights into acquisition, retention, and product recommendations. 
                                                                                                                                 
## Data                                                                                                                          
                                                                                                                                 
The project uses the public Olist Brazilian E‑Commerce dataset from Kaggle:                                                       

 • Olist dataset main page [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce].                                         

Due to licensing and file size, the raw CSV files are not included in this repository.                                            

To run the analysis:                                                                                                              

 1 Download the dataset from Kaggle.                                                                                              
 2 Place at least the following CSV files into a local data/ folder:                                                              
    • olist_orders_dataset.csv                                                                                                    
    • olist_order_payments_dataset.csv                                                                                            
    • olist_customers_dataset.csv                                                                                                 
 3 (Optional) To extend the analysis, also include:                                                                               
    • olist_order_items_dataset.csv                                                                                               
    • olist_products_dataset.csv                                                                                                  
    • olist_sellers_dataset.csv                                                                                                   
    • olist_order_reviews_dataset.csv 
                                                                                                                                  
## Methods                                                                                                                       
                                                                                                                                  
1 Order and customer tables                                                                                                      
    • Filter to delivered orders (common for revenue and LTV analysis).                                                           
    • Aggregate olist_order_payments_dataset to compute order_revenue per order_id.                                               
    • Join orders with customers to obtain customer_unique_id and customer_state.                                                 
    • Build a customer‑level summary table with:                                                                                  
       • first_order_date and cohort_month (first order month).                                                                   
       • n_orders (number of orders per customer).                                                                                
       • total_revenue (total realised revenue per customer).                                                                     
 2 Cohort and retention analysis                                                                                                  
    • Define cohorts by cohort_month = first_order_date.to_period("M").                                                           
    • Compute t_months = months since first order for each order.                                                                 
    • For each cohort_month × t_months, compute:                                                                                  
       • Total revenue.                                                                                                           
       • Revenue per original cohort customer (total revenue ÷ cohort size).                                                      
       • Retention rate: fraction of original cohort customers who have placed at least one order by that month.                  
    • Visualise:                                                                                                                  
       • Cohort revenue heatmap (average revenue per customer over time).                                                         
       • Cumulative LTV per customer heatmap (cumulative revenue by cohort × months since first order).                           
       • Retention heatmap (retention rate by cohort × months).                                                                   
 3 LTV₁₂ₘ definition and feature engineering                                                                                      
    • Define LTV₁₂ₘ as the total revenue a customer generates in the first 12 months after their first purchase:                  
       • Sum of order_revenue for t_months ∈ [0, 11].                                                                             
    • Engineer early‑behaviour features per customer:                                                                             
       • rev_1m, n_orders_1m: revenue and number of orders in the first month (t_months = 0).                                     
       • rev_3m, n_orders_3m: revenue and number of orders in the first 3 months (t_months ∈ [0, 2]).                             
    • Merge these features with the customer summary and LTV₁₂ₘ label to form the modeling dataset.                               
 4 LTV₁₂ₘ modeling                                                                                                                
    • Target: continuous LTV₁₂ₘ.                                                                                                  
    • Features used in the baseline model:                                                                                        
       • Cohort month (as a categorical feature).                                                                                 
       • Customer state (geography).                                                                                              
       • Early‑behaviour features (rev_1m, n_orders_1m, rev_3m, n_orders_3m).                                                     
    • Model:                                                                                                                      
       • Gradient Boosting Regressor (Scikit‑Learn), trained on log(LTV₁₂ₘ + 1) to reduce the effect of the heavy right tail.     
    • Evaluation:                                                                                                                 
       • Random train/test split on customers (simple baseline; can be extended to a time‑based split).                           
       • Metrics: mean absolute error (MAE) and root mean squared error (RMSE) on the original LTV₁₂ₘ scale.  
                                                                                                                                  
## Results & Insights (Summary)                                                                                                  
                                                                                                                                  
Cohort revenue and LTV curves                                                                                                     

 • Revenue per customer is heavily front‑loaded.                                                                                  
    • Most cohorts realise the majority of their LTV within the first 6–12 months after acquisition.                              
    • After ≈ 6–9 months, incremental revenue per customer flattens for most cohorts.                                             
 • The cumulative LTV heatmap and selected cohort curves show that:                                                               
    • A large share of total LTV is accumulated early in the customer lifecycle.                                                  
    • Some cohorts have systematically higher 12‑month LTV per customer than others, suggesting differences in acquisition        
      channels, product experience, or macro conditions.                                                                          

Retention patterns                                                                                                                

 • Retention starts at 100% at t_months = 0 by construction (all customers make at least one purchase in their cohort month).     
 • Retention drops sharply in the first few months, with:                                                                         
    • Many one‑time buyers.                                                                                                       
    • A smaller base of repeat customers that drive most of the long‑run revenue.                                                 
 • This pattern is typical for e‑commerce and marketplace businesses: a long tail of low‑engagement users and a small, valuable   
   core of repeat purchasers.                                                                                                     

LTV₁₂ₘ distribution                                                                                                               

 • Among roughly 93,000 customers, the LTV₁₂ₘ distribution is:                                                                    
    • Median LTV₁₂ₘ ≈ 108.                                                                                                        
    • Mean LTV₁₂ₘ ≈ 165.                                                                                                          
    • 25th percentile ≈ 63, 75th percentile ≈ 182.                                                                                
    • Maximum LTV₁₂ₘ > 13,600.                                                                                                    
 • The distribution is highly skewed, with a small number of “whale” customers who generate very high revenue compared to the     
   median.                                                                                                                        

LTV₁₂ₘ model performance (baseline)                                                                                               

 • Baseline Gradient Boosting model using cohort, state, and early‑behaviour features achieves approximately:                     
    • MAE ≈ 3.7.                                                                                                                  
    • RMSE ≈ 59.3.                                                                                                                
 • Relative to a median LTV₁₂ₘ of about 108, the MAE is only ≈ 3–4% of a typical customer’s LTV, indicating very accurate         
   predictions for the majority of customers.                                                                                     
 • The higher RMSE is driven by a small number of very high‑LTV outliers, which is expected given the heavy tail of the LTV₁₂ₘ    
   distribution.      
                                                                                                                                  
## Business Recommendations (Brief)                                                                                              
                                                                                                                                  
 1 Prioritise early‑life engagement                                                                                               
    • Because most LTV is realised in the first 6–12 months and early behaviour (first 1–3 months) is highly predictive of LTV₁₂ₘ,
      onboarding and early‑life engagement should be a priority.                                                                  
    • Practical actions for a marketplace or e‑commerce platform:                                                                 
       • Encourage a second purchase within the first 30–60 days using personalised recommendations and targeted offers.          
       • Experiment with onboarding flows that expose customers to high‑retention categories or high‑quality sellers early.       
 2 Allocate acquisition budget by cohort quality                                                                                  
    • Cohort differences in cumulative LTV suggest that some acquisition periods, regions, or channels bring in systematically    
      higher‑value customers.                                                                                                     
    • Instead of using a single average CAC target, marketing teams can:                                                          
       • Allocate more budget to channels and segments whose cohorts show higher LTV₁₂ₘ.                                          
       • Reduce spend or adjust targeting for cohorts with low realised or predicted LTV.                                         
 3 Use LTV predictions in retention and CRM strategies                                                                            
    • Integrating LTV₁₂ₘ predictions into CRM / marketing automation pipelines enables:                                           
       • Early identification of high‑potential customers for enhanced experiences, loyalty programmes, or personalised           
         communication.                                                                                                           
       • Avoiding over‑investment in low‑value segments where incremental spend is unlikely to be recovered.                      
       • Monitoring how changes to onboarding, UX, pricing, or recommendations affect predicted LTV across cohorts over time.                                                                                                                                    
## Repository Structure                                                                                                          
                                                                                                                                  
 - `notebooks/ltv_olist_analysis.ipynb` – main analysis notebook (EDA, cohorts, LTV, modeling).                                   
 - `data/` – folder for raw CSV files (not tracked in git).                                                                       
 - `README.md` – project overview, methods, and results.                                                                          
 - `requirements.txt` – Python dependencies.                                                                                      
                                                                                                                                  
## How to Run                                                                                                                    
                                                                                                                                  
 1 Create and activate a Python environment (for example, with venv or conda).                                                    
   Example using venv:                                                                                                            
                                                                                                                                  
    python -m venv venv                                                                                                           
    source venv/bin/activate   # on macOS / Linux                                                                                 
    # venv\Scripts\activate    # on Windows                                                                                       
                                                                                                                                  
 2 Install dependencies:                                                                                                          
                                                                                                                                  
    pip install -r requirements.txt                                                                                               
                                                                                                                                  
 3 Download the Olist dataset from Kaggle and place the required CSV files into the data/ folder as described in the Data section.
 4 Open notebooks/ltv_olist_analysis.ipynb in Jupyter, JupyterLab, or VS Code, and run all cells to reproduce the analysis and    
   figures.                                                                                                          

## Next Steps and Possible Extensions                                                                                                

Planned or suggested extensions to make this project even closer to a production‑ready marketplace analytics engine:              

 • Replace the random train/test split with a strict time‑based split on first_order_date to better mimic real deployment.        
 • Add richer features (product category mix, early basket size, inter‑purchase times, basic seller attributes) and compare       
   additional models such as Random Forests or XGBoost.                                                                           
 • Evaluate business‑oriented metrics such as:                                                                                    
    • LTV₁₂ₘ prediction accuracy by true LTV decile.                                                                              
    • Share of total revenue captured by the top 10% of customers ranked by predicted LTV.                                        
 • Build cohort‑level demand forecasts (predict future cohort revenue from the first 3–6 months of behaviour) to support budgeting
   and capacity planning.                                                                                                         
 • Expose the trained LTV model via a simple API or Streamlit dashboard to demonstrate how a product or CRM team could consume the
   predictions in practice.  


   
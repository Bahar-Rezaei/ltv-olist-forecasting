
# Dockerfile                 
FROM python:3.10-slim                                                                                                                                                 
WORKDIR /app 
                 
# system deps for pandas/sklearn if needed                 
RUN apt-get update && apt-get install -y build-essential gcc --no-install-recommends \                  
    && rm -rf /var/lib/apt/lists/*    
    
COPY requirements.txt .                 
RUN pip install --no-cache-dir -r requirements.txt 

COPY app/ ./app/  
COPY models/ ./models/ 

EXPOSE 8000  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
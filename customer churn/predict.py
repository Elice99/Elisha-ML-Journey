import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# ======================
# Load model
# ======================
model_file = "model_C=1.0.bin"

with open(model_file, "rb") as f_in:
    dv, model = pickle.load(f_in)

# ======================
# FastAPI app
# ======================
app = FastAPI(
    title="Customer Churn API",
    description="Predict customer churn using ML model",
    version="1.0"
)

# ======================
# Input schema (Swagger form)
# ======================
class CustomerInput(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract: str
    
    
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Customer Churn Prediction API",
        "docs": "/docs"
    }
    
@app.post("/predict")
def predict(customer: CustomerInput):

    # convert input to dict
    customer_dict = customer.dict()

    # transform using your DictVectorizer
    X = dv.transform([customer_dict])

    # predict probability
    y_pred = model.predict_proba(X)[0, 1]

    return {
        "churn_probability": float(y_pred),
        "churn": y_pred >= 0.5
    }


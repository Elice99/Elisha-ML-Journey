import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Load model and DictVectorizer
model_file = 'wallet_classifer=1.0.bin'
with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = FastAPI(title="Wallet Prediction API")

# Define Pydantic model for input validation - adapt fields and types as needed
class WalletInfo(BaseModel):
    tx_count_365d: Optional[float]
    vol_per_tx: Optional[float]
    activity_per_week: Optional[float]
    avg_weekly_vol: Optional[float]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wallet Prediction API! Use POST /predict with JSON input."}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/predict")
def predict(wallet_info: WalletInfo):
    # Convert Pydantic model to dict and transform
    data_dict = wallet_info.dict()
    X = dv.transform([data_dict])
    y_pred = model.predict_proba(X)[0, 1]
    good_trader = y_pred >= 0.7

    return {
        "good_trader_probability": float(y_pred),
        "good_trader": bool(good_trader)
    }

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9696, reload=True)


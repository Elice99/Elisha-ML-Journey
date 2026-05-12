# Customer Churn Prediction Model - Technical Documentation

## Executive Summary

This project implements a machine learning pipeline to predict customer churn for a telecommunications provider using logistic regression. The solution encompasses data preprocessing, model training with cross-validation, evaluation metrics, and a production-ready REST API for real-time predictions.

---

## Project Architecture

### 1. Data Pipeline (`Churn.py`)

#### Data Source
- **Dataset**: Telco-Customer-Churn.csv
- **Records**: ~7,000 customer observations
- **Features**: 21 attributes covering demographics, services, and billing information

#### Data Cleaning & Preprocessing
```
Step 1: Column Normalization
  - Convert all column names to lowercase
  - Replace spaces with underscores for consistency
  
Step 2: Categorical Data Processing
  - Standardize all string values to lowercase
  - Remove whitespace from categorical features
  
Step 3: Numerical Data Handling
  - Convert 'totalcharges' to numeric (coerce errors to NaN)
  - Fill missing values with 0 (imputation strategy)
  
Step 4: Target Variable Engineering
  - Convert 'churn' from binary strings ('yes'/'no') to integers (1/0)
  
Step 5: Data Splitting
  - Train-test split: 80-20 ratio (random_state=1 for reproducibility)
  - Full training set: 5,634 records
  - Test set: 1,409 records
```

#### Feature Sets

**Numerical Features (3)**:
- `tenure`: Customer account duration in months
- `monthlycharges`: Monthly billing amount
- `totalcharges`: Cumulative charges

**Categorical Features (16)**:
- Demographics: gender, seniorcitizen, partner, dependents
- Services: phoneservice, multiplelines, internetservice
- Add-on Services: onlinesecurity, onlinebackup, deviceprotection, techsupport, streamingtv, streamingmovies
- Account Info: contract, paperlessbilling, paymentmethod

---

### 2. Model Training & Validation

#### Algorithm: Logistic Regression
- **Solver**: LBFGS (default)
- **Regularization Parameter (C)**: 1.0 (inverse of regularization strength)
- **Max Iterations**: 5,000 (notebook uses 1,000, main script uses 5,000)
- **Sparse Output**: False (dense feature matrix)

#### Feature Engineering
```python
DictVectorizer()
  ├─ Converts feature dictionaries to numerical matrices
  ├─ One-hot encodes categorical variables
  └─ Handles missing features gracefully
```

#### Validation Strategy: K-Fold Cross-Validation
- **Number of Splits**: 5
- **Shuffle**: True
- **Random State**: 1 (reproducibility)
- **Metrics**: ROC-AUC Score

#### Results

**Validation Performance** (K-Fold):
```
C=1.0:  AUC = 0.842 ± 0.007
Fold 0: AUC = 0.8446
Fold 1: AUC = 0.8452
Fold 2: AUC = 0.8335
Fold 3: AUC = 0.8348
Fold 4: AUC = 0.8516
```

**Test Set Performance**:
```
AUC = 0.8583
```

#### Interpretation
- **ROC-AUC of 0.858**: Model correctly ranks a random churner higher than a random non-churner 85.8% of the time
- **Consistency**: Validation and test AUC are closely aligned, indicating minimal overfitting
- **Production Readiness**: Performance metrics suggest reliable real-world deployment

---

### 3. Model Serialization (`pickle`)

**File Format**: Binary pickle serialization
- **Artifacts Saved**: 
  - `DictVectorizer` (dv): Fitted feature transformer
  - `LogisticRegression` (model): Trained classifier

**File Output**: `model_C=1.0.bin`
- Contains both preprocessing and prediction logic
- Enables seamless inference without retraining

---

### 4. Production API (`predict.py`)

#### Framework: Flask
- **Lightweight REST framework** for model serving
- **Python-based** for easy deployment

#### Endpoint Specification

**Route**: `POST /predict`
- **Content-Type**: application/json
- **Host**: 0.0.0.0 (all network interfaces)
- **Port**: 9696

**Input Schema**:
```json
{
  "gender": "male",
  "seniorcitizen": 0,
  "partner": "yes",
  "dependents": "no",
  "tenure": 24,
  "phoneservice": "yes",
  "multiplelines": "no",
  "internetservice": "fiber_optic",
  "onlinesecurity": "no",
  "onlinebackup": "yes",
  "deviceprotection": "yes",
  "techsupport": "yes",
  "streamingtv": "yes",
  "streamingmovies": "yes",
  "contract": "month-to-month",
  "paperlessbilling": "yes",
  "paymentmethod": "electronic_check",
  "monthlycharges": 65.5,
  "totalcharges": 1570.0
}
```

**Output Schema**:
```json
{
  "churn_probability": 0.32,
  "churn": false
}
```

**Decision Threshold**: 0.5
- Probability ≥ 0.5 → Classified as churner
- Probability < 0.5 → Classified as retained customer

#### Request-Response Cycle
```
1. Accept JSON customer profile
2. Apply DictVectorizer transformation
3. Generate probability prediction
4. Apply decision threshold (0.5)
5. Return churn probability and binary classification
```

---

## Technical Stack

| Component | Tool/Library | Purpose |
|-----------|--------------|---------|
| **Data Processing** | pandas, numpy | Data manipulation & numerical operations |
| **ML Framework** | scikit-learn | Logistic regression & model validation |
| **Model Persistence** | pickle | Serialize/deserialize trained models |
| **Web Framework** | Flask | REST API for production serving |
| **Validation** | KFold, roc_auc_score | Cross-validation & performance metrics |

---

## Known Issues & Considerations

### 1. Convergence Warnings
- **Issue**: Logistic regression fails to converge in notebook (max_iter=1000)
- **Solution**: Main script increased to max_iter=5000
- **Recommendation**: Consider feature scaling or alternative solvers for larger datasets

### 2. Data Imputation Strategy
- **Current**: Missing `totalcharges` filled with 0
- **Risk**: May bias predictions for new customers (low tenure)
- **Alternative**: Use median/mean imputation or median/mode based on customer segment

### 3. Feature Sparsity
- **Note**: Month-to-month contracts represent 55% of data (class imbalance risk)
- **Mitigation**: Consider weighted loss functions or resampling for highly imbalanced future datasets

### 4. Decision Threshold
- **Current**: Binary classification at 0.5 probability
- **Flexibility**: Can be adjusted based on business cost-benefit (retention cost vs. churn cost)

---

## Deployment Guidelines

### Prerequisites
```bash
pip install pandas numpy scikit-learn flask
```

### Running the API
```bash
python predict.py
```

### Testing the API
```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "yes",
    "tenure": 36,
    "phoneservice": "yes",
    "multiplelines": "yes",
    "internetservice": "dsl",
    "onlinesecurity": "yes",
    "onlinebackup": "no",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "two_year",
    "paperlessbilling": "no",
    "paymentmethod": "bank_transfer",
    "monthlycharges": 45.0,
    "totalcharges": 1620.0
  }'
```

### Expected Response
```json
{
  "churn_probability": 0.12,
  "churn": false
}
```

---

## Future Enhancements

1. **Hyperparameter Optimization**
   - GridSearchCV for regularization strength (C parameter)
   - Explore alternative algorithms (Random Forest, XGBoost)

2. **Feature Engineering**
   - Customer lifetime value (CLV) scoring
   - Engagement metrics (support ticket frequency)
   - Temporal features (seasonal patterns)

3. **Model Monitoring**
   - Prediction distribution tracking
   - Performance degradation alerts
   - Retraining pipelines

4. **API Enhancement**
   - Batch prediction endpoint
   - Feature importance explanations (SHAP/LIME)
   - Confidence intervals for predictions

5. **Production Deployment**
   - Containerization (Docker)
   - Cloud hosting (AWS, GCP, Azure)
   - Model versioning & A/B testing

---

## Files Overview

| File | Purpose |
|------|---------|
| `Churn.py` | Production pipeline for training & validation |
| `Classification.ipynb` | Exploratory & interactive model development |
| `predict.py` | Flask API for inference |
| `model_C=1.0.bin` | Serialized trained model & vectorizer |

---

## Performance Metrics Summary

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| **Validation AUC** | 0.842 | Strong discriminative ability across folds |
| **Test AUC** | 0.858 | Reliable generalization to unseen data |
| **Standard Deviation** | 0.007 | Stable performance across splits |
| **Decision Threshold** | 0.50 | Balanced sensitivity/specificity |

---

## References

- scikit-learn Logistic Regression: https://scikit-learn.org/stable/modules/linear_model.html
- ROC-AUC Interpretation: https://en.wikipedia.org/wiki/Receiver_operating_characteristic
- Flask Documentation: https://flask.palletsprojects.com/

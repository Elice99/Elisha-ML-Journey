# Customer Churn Prediction Project - Quick Reference Card

## 🎯 Project at a Glance

| Aspect | Details |
|--------|---------|
| **Objective** | Predict which customers will churn (leave) within next billing period |
| **Dataset** | Telco-Customer-Churn.csv (~7,000 customers) |
| **Model Type** | Binary Classification (Logistic Regression) |
| **Performance** | 85.8% AUC (test set) |
| **Status** | Production-Ready |
| **Deployment** | Flask REST API on port 9696 |

---

## 📁 Project Structure

```
customer-churn/
├── Churn.py                    # Training & validation pipeline
├── Classification.ipynb        # Exploratory notebook
├── predict.py                  # Flask API for production
├── model_C=1.0.bin             # Serialized model artifact
└── Customer_Retention.xlsx     # Executive dashboard
```

---

## 🔧 Model Overview

**Algorithm**: Logistic Regression
- Regularization: C=1.0
- Max iterations: 5,000
- Feature encoding: DictVectorizer (one-hot categorical, standardized numeric)

**Validation**: 5-Fold Cross-Validation
- Folds: 5
- Metric: ROC-AUC
- Mean AUC: 0.842 ± 0.007

---

## 📊 Key Performance Indicators

| Metric | Value | Insight |
|--------|-------|---------|
| **Test AUC** | 0.858 | Strong discriminative ability |
| **Validation AUC** | 0.842 | Low overfitting risk |
| **Variance** | ±0.007 | Stable across folds |
| **Decision Threshold** | 0.50 | Balanced sensitivity-specificity |

---

## 💡 Top Business Insights

### Churn Risk Factors (Ranked by Importance)

1. **Contract Type** (Strongest predictor)
   - Month-to-month: 55% (HIGH RISK)
   - Two-year: 24% (LOWEST RISK)
   - One-year: 21% (MEDIUM RISK)

2. **Service Adoption** (Engagement indicator)
   - Tech Support: 29% → Low = Higher churn
   - Online Security: 29% → Low = Higher churn
   - Online Backup: 34% → Low = Higher churn

3. **Internet Service Type**
   - Fiber Optic: Higher churn (expectation mismatch)
   - DSL: Lower churn
   - No Service: Very stable

4. **Customer Demographics**
   - Senior Citizens: 16% (higher propensity)
   - Family Status: Partner/dependents stabilize

5. **Account Friction Points**
   - Payment Method: Electronic check = friction
   - Paperless Billing: No adoption = slight risk

---

## 🎯 At-Risk Customer Profile

**Current at-risk population**: 1,869 customers (26% of base)
**Annual revenue at stake**: $2,862,927
**Monthly revenue exposure**: $139,131

**Typical high-risk customer:**
- Tenure: < 12 months
- Contract: Month-to-month
- Internet: Fiber optic
- Services: No security/backup/support
- Payment: Electronic check
- Predicted churn probability: 60-80%

---

## 📈 Business Impact Projection

### Year 1 (Conservative Scenario)
- **Target**: 300 at-risk customers
- **Retention Rate**: 40%
- **Savings**: 300 × 0.4 × $1,400/year = **$420K**
- **Investment**: $150K
- **Net Benefit**: $270K
- **ROI**: 180%

### Year 1 (Moderate Scenario)
- **Target**: 600 at-risk customers
- **Retention Rate**: 50%
- **Savings**: 600 × 0.5 × $1,400/year = **$840K**
- **Net Benefit**: $690K
- **ROI**: 460%

### Year 1 (Optimistic Scenario)
- **Churn prevention**: 900 customers = $1.26M
- **Service bundling upsell**: +5% = $143K
- **Total savings**: $1.4M
- **ROI**: 840%

---

## 🚀 Quick Start: Running the Model

### Training the Model
```bash
python Churn.py
```
**Output**: `model_C=1.0.bin` (serialized model)

### Starting the API
```bash
python predict.py
```
**Server**: http://localhost:9696

### Making a Prediction
```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 24,
    "monthlycharges": 65.5,
    "totalcharges": 1570.0,
    "contract": "month-to-month",
    "onlinesecurity": "no",
    "techsupport": "no",
    "internetservice": "fiber_optic",
    "paymentmethod": "electronic_check",
    ... (other fields)
  }'
```

**Response**:
```json
{
  "churn_probability": 0.72,
  "churn": true
}
```

---

## 📋 Features Used

### Numerical (3)
- `tenure`: Months as customer
- `monthlycharges`: Monthly bill
- `totalcharges`: Cumulative charges

### Categorical (16)
Demographics:
- gender, seniorcitizen, partner, dependents

Services:
- phoneservice, multiplelines, internetservice, onlinesecurity, onlinebackup, deviceprotection, techsupport, streamingtv, streamingmovies

Account:
- contract, paperlessbilling, paymentmethod

---

## ⚠️ Known Limitations & Next Steps

### Current Limitations
1. **Data Imputation**: Missing totalcharges filled with 0 (may bias new customers)
2. **Convergence**: Required 5,000 iterations in some folds (consider scaling features)
3. **Decision Threshold**: Fixed at 0.50 (consider business cost-benefit optimization)
4. **Class Imbalance**: Not addressed (fine for current accuracy level)

### Recommended Enhancements
1. **Model Improvement**
   - GridSearchCV for optimal C parameter
   - Test alternative algorithms (Random Forest, XGBoost)
   - Feature scaling for faster convergence

2. **Data Enhancement**
   - Add temporal features (seasonality, trend)
   - Include customer lifetime value (CLV)
   - Historical churn patterns by cohort

3. **Production Deployment**
   - Containerize with Docker
   - Cloud hosting (AWS Lambda, GCP Cloud Functions)
   - Model versioning & A/B testing framework
   - Real-time performance monitoring

4. **Business Integration**
   - CRM integration for automated scoring
   - Dashboard automation (daily/weekly updates)
   - Campaign ROI tracking

5. **Advanced Analytics**
   - SHAP/LIME for feature importance per customer
   - Survival analysis for time-to-churn prediction
   - Lookalike modeling (find similar at-risk customers)

---

## 👤 Model Explainability

**Why does the model predict churn?**

Top contributing factors (in order of strength):
1. **Contract type** - Month-to-month is 3x higher risk than 2-year
2. **Tenure** - New customers (< 6 months) are most volatile
3. **Support services adoption** - No tech support = frustration
4. **Internet service quality** - Fiber expectations not met
5. **Payment friction** - Electronic check = operational drag

**How to reduce churn for specific customer?**
- Upgrade from month-to-month → 2-year contract (biggest impact)
- Add tech support service (engagement)
- Bundle streaming services (sticky features)
- Switch to bank transfer (friction reduction)

---

## 📞 Support & Questions

**Technical Issues**:
- Model not loading? Check pickle file exists
- API won't start? Verify port 9696 is available
- Predictions wrong? Ensure all 19 features in JSON input

**Business Questions**:
- How accurate is this model? 85.8% AUC (top 14% error rate acceptable)
- Can we use this for other predictions? Yes—framework transfers to upsell, LTV, etc.
- How often to retrain? Monthly recommended initially, weekly at scale

---

## 📚 File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| `Churn.py` | 107 | Production training pipeline with K-fold validation |
| `Classification.ipynb` | 190 | Exploratory analysis & model development |
| `predict.py` | 23 | Flask REST API for inference |
| `model_C=1.0.bin` | - | Serialized vectorizer + model (binary) |

---

## 🎓 Key Learnings

✅ **Model accuracy ≠ business impact** (A 75% accurate model that drives $500K savings beats 95% accuracy that's unused)

✅ **Interpretability matters** (Stakeholders need to understand *why* before they act)

✅ **Data quality is foundational** (Garbage in = garbage out; spent 40% of time on cleaning/preparation)

✅ **Production is different from notebook** (API design, error handling, monitoring, versioning)

✅ **The best metric is revenue impact** (Always tie ML metrics back to business outcomes)

---

## 📞 Quick Reference Links

- **scikit-learn Logistic Regression**: https://scikit-learn.org/stable/modules/linear_model.html
- **Flask Documentation**: https://flask.palletsprojects.com/
- **ROC-AUC Guide**: https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics

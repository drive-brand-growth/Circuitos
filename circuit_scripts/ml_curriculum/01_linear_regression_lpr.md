# Linear Regression - LPR Score Predictor
**ML Curriculum Circuit #1**

## From ML Algorithms Overview

**Theory:**
- "Mother of all ML algorithms"
- Finds linear relationship between input and output variables
- Minimizes sum of squares of distances between data points and regression line
- Many fancy ML algorithms (including neural networks) are extensions of this simple idea

## Circuit OS Learning Objective

Learn how linear regression predicts LPR (Lead Probability to Revenue) scores based on:
- Engagement score
- Company size
- Geographic fit
- Website traffic

## Steps

### 1. Theory Overview

**Linear Regression Equation:**
```
LPR_Score = β₀ + β₁(engagement) + β₂(company_size) + β₃(geo_fit) + β₄(traffic)
```

Where:
- β₀ = intercept (base score)
- β₁, β₂, β₃, β₄ = coefficients (feature weights)

**Goal:** Find coefficients that minimize prediction error

---

### 2. Prepare Training Data

```python
# Simulated Circuit OS lead data
training_data = [
    {
        "engagement_score": 75,
        "company_size": 150,
        "geographic_fit": 0.85,
        "website_traffic": 80000,
        "actual_lpr_score": 87  # Real conversion score
    },
    {
        "engagement_score": 45,
        "company_size": 20,
        "geographic_fit": 0.42,
        "website_traffic": 5000,
        "actual_lpr_score": 42
    },
    # ... 1000+ more leads with outcomes
]
```

**Action:** Load real lead data from Circuit OS database

---

### 3. Train Linear Regression Model

```python
from circuit_os_ml_service.intelligence.ml_service import MLService

ml_service = MLService()

# Train model
result = await ml_service.trainer.train_regressor(
    X=training_features,  # [[75, 150, 0.85, 80000], ...]
    y=training_labels,  # [87, 42, ...]
    algorithms=["linear_regression"]  # Only linear regression
)

print(f"RMSE: {result['rmse']:.2f}")
print(f"R²: {result['r2']:.3f}")
```

**Interpretation:**
- **RMSE = 12.4:** Predictions within ±12.4 points of actual score
- **R² = 0.76:** Model explains 76% of variance in LPR scores

---

### 4. Understand Coefficients

```python
model = result['model']

coefficients = {
    "engagement_score": model.coef_[0],  # e.g., 0.35
    "company_size": model.coef_[1],  # e.g., 0.08
    "geographic_fit": model.coef_[2],  # e.g., 25.0
    "website_traffic": model.coef_[3]  # e.g., 0.0002
}

# Interpretation:
# For every 1 point increase in engagement_score → LPR increases by 0.35
# For every additional employee → LPR increases by 0.08
# For every 0.1 increase in geographic_fit → LPR increases by 2.5
```

**Business Insight:** Geographic fit has the strongest impact on conversion!

---

### 5. Make Predictions

```python
new_lead = {
    "engagement_score": 68,
    "company_size": 95,
    "geographic_fit": 0.72,
    "website_traffic": 45000
}

predicted_lpr = model.predict([[68, 95, 0.72, 45000]])
# Output: 74.2

print(f"Predicted LPR Score: {predicted_lpr[0]:.1f}")
print(f"Conversion Probability: {predicted_lpr[0]}%")
```

**Action:** Move lead to "Medium Priority" queue

---

### 6. Compare to Ground Truth

After 24 hours, check actual outcome:
```python
actual_outcome = {
    "converted": True,
    "actual_lpr_score": 78
}

error = abs(predicted_lpr[0] - actual_outcome['actual_lpr_score'])
print(f"Prediction Error: {error:.1f} points")
# Output: 3.8 points (very accurate!)
```

---

### 7. Visualize Linear Relationship

```python
# Plot engagement_score vs LPR score
import matplotlib.pyplot as plt

plt.scatter(X[:, 0], y, alpha=0.5, label='Actual')
plt.plot(X[:, 0], model.predict(X), color='red', label='Linear Fit')
plt.xlabel('Engagement Score')
plt.ylabel('LPR Score')
plt.title('Linear Regression: Engagement → LPR Score')
plt.legend()
plt.show()
```

---

## Key Takeaways

### ✅ Why Linear Regression Works for LPR

1. **Simple:** Easy to understand and explain to stakeholders
2. **Fast:** Trains in milliseconds on 10K+ leads
3. **Interpretable:** Feature coefficients show what matters
4. **Baseline:** Many advanced algorithms are extensions of this

### ❌ When Linear Regression Fails

- Non-linear relationships (exponential, polynomial)
- Complex interactions between features
- Small datasets with noise
- When you need maximum accuracy (use XGBoost instead)

### 🎯 Circuit OS Production Use

```python
# Use linear regression for:
- Quick LPR score estimates
- Feature importance analysis
- A/B test baseline model
- When interpretability > accuracy

# Upgrade to XGBoost when:
- Need maximum accuracy
- Have large dataset (10K+ leads)
- Complex patterns exist
```

---

## Next Steps

1. ✅ Complete this linear regression tutorial
2. ➡️ Move to Circuit #2: Logistic Regression for binary classification
3. ➡️ Compare linear regression vs gradient boosting (Circuit #3)
4. ➡️ Learn clustering for customer segmentation (Circuit #4)

---

**Status:** ✅ Linear Regression Tutorial Complete
**ML Concept:** Regression (predict continuous values)
**Circuit OS Integration:** LPR Score Prediction
**Time to Complete:** 30-45 minutes

---

**© 2025 CircuitOS™ - ML Education Series**

# Classification - Intent Prediction
**ML Curriculum Circuit #2**

## From ML Algorithms Overview

**Classification:** Assign discrete categorical labels to data points
- Example: Spam vs not spam, high-intent vs low-intent
- Algorithms: Logistic Regression, Random Forest, Naive Bayes, SVM

## Circuit OS Learning Objective

Classify lead intent based on conversation patterns:
- **"pricing_inquiry"** → High intent, ready to buy
- **"general_info"** → Medium intent, researching
- **"complaint"** → Low intent, support issue
- **"spam"** → No intent, junk inquiry

## Steps

### 1. Prepare Classification Data

```python
training_data = [
    {
        "message": "What are your rates for 10+ memberships?",
        "features": {
            "contains_pricing_words": 1,
            "question_marks": 1,
            "word_count": 7,
            "mentions_quantity": 1
        },
        "label": "pricing_inquiry"  # Target class
    },
    {
        "message": "Thanks for the info",
        "features": {
            "contains_pricing_words": 0,
            "question_marks": 0,
            "word_count": 4,
            "mentions_quantity": 0
        },
        "label": "general_info"
    }
]
```

### 2. Compare Classification Algorithms

```python
from circuit_os_ml_service.intelligence.ml_service import MLService

ml_service = MLService()

# Train ALL classification algorithms
result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels
)

print(f"Best Algorithm: {result['model_type']}")
print(f"Accuracy: {result['accuracy']:.1%}")
print(f"F1 Score: {result['f1_score']:.3f}")
```

**Results:**
```
Algorithm Comparison:
├── Logistic Regression: 84.2% accuracy
├── KNN: 78.5% accuracy
├── Naive Bayes: 86.1% accuracy ← BEST for text!
├── Random Forest: 82.7% accuracy
├── Gradient Boosting: 85.3% accuracy
└── XGBoost: 87.2% accuracy ← BEST overall
```

### 3. Why Naive Bayes Wins for Text

From ML Algorithms Overview:
> "Naive Bayes counts word occurrences in different classes and multiplies probabilities. It's computationally efficient and a good approximation for text-based tasks."

```python
# Naive Bayes for "What are your rates?"
word_probabilities = {
    "rates": {
        "pricing_inquiry": 0.82,  # 82% of pricing inquiries mention "rates"
        "general_info": 0.15
    },
    "your": {
        "pricing_inquiry": 0.65,
        "general_info": 0.60
    }
}

# Multiply probabilities
pricing_score = 0.82 * 0.65 = 0.533
general_score = 0.15 * 0.60 = 0.090

# Winner: pricing_inquiry (53.3% > 9%)
```

### 4. Make Predictions with Confidence

```python
new_message = "Can I book a free session today?"

# Extract features
features = extract_features(new_message)

# Predict
prediction = model.predict([features])
confidence = model.predict_proba([features]).max()

print(f"Intent: {prediction[0]}")  # "conversion_ready"
print(f"Confidence: {confidence:.1%}")  # 94%

# Business action
if prediction[0] == "conversion_ready" and confidence > 0.8:
    print("ACTION: Escalate to sales team immediately")
```

### 5. Confusion Matrix Analysis

```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

"""
                  Predicted
                  pricing  general  complaint  spam
Actual pricing       145      8        2        0
       general        12     98        5        1
       complaint       3      7       52        2
       spam            0      2        1       34

Accuracy by class:
- pricing_inquiry: 145/155 = 93.5%
- general_info: 98/116 = 84.5%
- complaint: 52/64 = 81.3%
- spam: 34/37 = 91.9%
"""
```

**Insight:** Model confuses "general" and "pricing" 8% of the time → retrain with more examples

## Key Takeaways

### Algorithm Selection for Intent Classification

| Algorithm | Accuracy | Speed | Interpretability | Best For |
|-----------|----------|-------|------------------|----------|
| **Naive Bayes** | 86% | ⚡⚡⚡ | ⭐⭐ | Text classification, fast predictions |
| **Logistic Regression** | 84% | ⚡⚡⚡ | ⭐⭐⭐ | Probability scores, feature importance |
| **Random Forest** | 83% | ⚡⚡ | ⭐ | Robust, handles missing data |
| **XGBoost** | 87% | ⚡ | ⭐ | Maximum accuracy |

### Production Deployment

```python
# Circuit OS production flow
async def classify_lead_intent(message: str):
    # 1. Extract features
    features = extract_features(message)

    # 2. Predict with trained model
    intent = naive_bayes_model.predict([features])[0]
    confidence = naive_bayes_model.predict_proba([features]).max()

    # 3. Route based on intent
    if intent == "pricing_inquiry" and confidence > 0.7:
        await escalate_to_sales(message, urgency="high")
    elif intent == "complaint":
        await route_to_support(message)
    elif intent == "spam":
        await mark_as_spam(message)
    else:
        await send_to_ai_responder(message)

    # 4. Track outcome for ML feedback loop
    await ml_service.record_outcome(
        model_name="intent_classifier",
        features=features,
        prediction=intent
    )
```

## Next Steps

1. ✅ Complete intent classification tutorial
2. ➡️ Circuit #3: Ensemble methods (Random Forest vs XGBoost)
3. ➡️ Circuit #4: Unsupervised learning (customer clustering)

---

**© 2025 CircuitOS™ - ML Education Series**

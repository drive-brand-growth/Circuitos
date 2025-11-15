# ML Algorithms Reference - Circuit OS Implementation Guide
**From Overview to Production**

**Version:** 2.0
**Date:** November 15, 2025
**Integration:** Links ML Algorithms Overview to Circuit OS code

---

## 📚 Quick Reference Table

| Algorithm | Type | Circuit OS File | Use Case | When to Use |
|-----------|------|----------------|----------|-------------|
| **Linear Regression** | Regression | `ml_service.py:310` | LPR scoring | Small datasets, interpretability |
| **Logistic Regression** | Classification | `ml_service.py:165` | Conversion prediction | Binary classification, probabilities |
| **K-Nearest Neighbors** | Both | `ml_service.py:166,313` | Lead similarity | Small datasets, recommendations |
| **Support Vector Machine** | Both | `ml_service.py:170-172,316-317` | Complex patterns | Non-linear relationships |
| **Naive Bayes** | Classification | `ml_service.py:167` | Email intent | Text classification |
| **Decision Tree** | Both | `ml_service.py:175,320` | Interpretable rules | Need explanations |
| **Random Forest** | Both | `ml_service.py:178,323` | Robust predictions | High dimensions, prevent overfitting |
| **AdaBoost** | Classification | `ml_service.py:182` | Sequential boost | Medium datasets |
| **Gradient Boosting** | Both | `ml_service.py:183,327` | High accuracy | Large datasets |
| **XGBoost** | Both | `ml_service.py:188,332` | Maximum accuracy | Production, competitions |
| **Neural Networks** | Both | `neural_network_service.py` | Complex patterns | Deep learning needed |
| **K-Means** | Clustering | `unsupervised_learning.py:40` | Segmentation | Find customer groups |
| **PCA** | Reduction | `unsupervised_learning.py:125` | Dimensionality | Reduce features 47→5 |

---

## 🎓 SUPERVISED LEARNING

### 1. Linear Regression
**"Mother of All ML Algorithms"**

**Theory from Overview:**
> Finds linear relationship between input and output variables by minimizing sum of squares of distances between data points and regression line. Many fancy ML algorithms (including neural networks) are extensions of this simple idea.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:310

result = await ml_service.trainer.train_regressor(
    X=features,  # [[engagement, company_size, geo_fit, traffic], ...]
    y=lpr_scores,  # [87, 42, 65, ...]
    algorithms=["linear_regression"]
)

# Equation learned:
# LPR = 50 + (0.35 * engagement) + (0.08 * company_size) + (25 * geo_fit)
```

**Use Cases:**
- LPR score prediction
- Revenue forecasting
- Feature importance analysis
- A/B test baseline

**When to Use:**
✅ Small datasets (< 500 samples)
✅ Need interpretability
✅ Linear relationships
✅ Fast training required

**When NOT to Use:**
❌ Complex non-linear patterns
❌ Need maximum accuracy
❌ Large datasets with interactions

---

### 2. Logistic Regression
**Binary Classification with Probabilities**

**Theory from Overview:**
> Variant of linear regression that fits a sigmoid function to predict categorical output. Provides probability of data point falling into a class.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:165

result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels,  # [1, 0, 1, 0, ...] (converted, not converted)
    algorithms=["logistic_regression"]
)

# Prediction
model = result['model']
probability = model.predict_proba([[features]])[0][1]  # 0.73 = 73% chance

print(f"Conversion Probability: {probability:.1%}")
# Output: "Conversion Probability: 73%"
```

**Use Cases:**
- Will lead convert? (yes/no)
- Spam vs not spam
- High-intent vs low-intent classification

**When to Use:**
✅ Binary classification
✅ Need probability scores
✅ Interpretable coefficients
✅ Small to medium datasets

---

### 3. K-Nearest Neighbors (KNN)
**Non-Parametric Similarity-Based**

**Theory from Overview:**
> Non-parametric algorithm that predicts based on K nearest neighbors. No true model fitting necessary. Prediction = average (regression) or majority vote (classification) of K neighbors.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:166,313

result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels,
    algorithms=["knn"]
)

# Find similar leads
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=5)
nn.fit(all_lead_features)

# For new lead, find 5 most similar leads
distances, indices = nn.kneighbors([new_lead_features])
similar_leads = leads[indices[0]]

# Predict based on similar leads
# If 4 out of 5 similar leads converted → 80% conversion probability
```

**Use Cases:**
- Lead similarity matching
- "Customers like this one also bought..."
- Recommendation systems

**When to Use:**
✅ Small datasets (< 5,000)
✅ Need similarity search
✅ No training time available
✅ Simple baseline

**Hyperparameters:**
- **K=3:** Small K, can overfit
- **K=5:** Good default
- **K=10:** Larger K, smoother predictions

---

### 4. Support Vector Machine (SVM)
**Maximum Margin with Kernel Trick**

**Theory from Overview:**
> Draws decision boundary that maximizes margin between classes. Uses kernel functions for implicit feature engineering via the kernel trick, allowing identification of highly complex nonlinear decision boundaries.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:170-172

result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels,
    algorithms=["svm_rbf"]  # RBF kernel for non-linear patterns
)

# Kernel options:
# - svm_linear: Linear decision boundary
# - svm_rbf: Radial basis function (most common)
# - svm_poly: Polynomial decision boundary
```

**Use Cases:**
- Complex pattern recognition
- Non-linear lead behavior
- High-dimensional data

**When to Use:**
✅ Medium datasets (1,000-10,000)
✅ Non-linear patterns
✅ High dimensions
✅ Need strong generalization

**When NOT to Use:**
❌ Large datasets (slow training)
❌ Need probability scores (SVM gives binary)
❌ Text data (use Naive Bayes)

---

### 5. Naive Bayes
**Fast Text Classification**

**Theory from Overview:**
> Based on Bayes' theorem. Calculates probability by multiplying word occurrences. "Naive" because assumes words are independent. Computationally efficient for text-based tasks.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:167

# Perfect for email intent classification
result = await ml_service.trainer.train_classifier(
    X=email_features,  # Word counts, TF-IDF vectors
    y=intent_labels,  # ["pricing", "general", "complaint", "spam"]
    algorithms=["naive_bayes"]
)

# Example: "What are your rates?"
P(pricing | "rates") = P("rates" | pricing) * P(pricing) / P("rates")
                     = 0.82 * 0.3 / 0.4
                     = 0.615 (61.5% chance it's pricing inquiry)
```

**Use Cases:**
- Email intent classification
- Spam filtering
- Sentiment analysis

**When to Use:**
✅ Text classification
✅ Need speed
✅ Limited training data
✅ Word-based features

---

### 6. Decision Tree
**Interpretable Yes/No Rules**

**Theory from Overview:**
> Series of yes/no questions that partition data into leaf nodes. Goal is to find splits that lead to pure leaf nodes, minimizing misclassification.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:175,320

result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels,
    algorithms=["decision_tree"]
)

# Visualize rules
from sklearn.tree import export_text
rules = export_text(result['model'], feature_names=feature_names)
print(rules)

"""
Output:
|--- pricing_page_visits <= 2.5
|   |--- engagement_score <= 50
|   |   |--- class: low_intent
|   |--- engagement_score > 50
|   |   |--- class: medium_intent
|--- pricing_page_visits > 2.5
|   |--- class: high_intent
"""
```

**Use Cases:**
- Explainable AI (stakeholder presentations)
- Rule-based classification
- Feature importance discovery

**When to Use:**
✅ Need interpretability
✅ Explain decisions to non-technical users
✅ Find threshold values

**When NOT to Use:**
❌ Need high accuracy (use Random Forest)
❌ Prone to overfitting on small data

---

### 7. Random Forest
**Ensemble of Decision Trees**

**Theory from Overview:**
> Many decision trees vote by majority. Random feature exclusion prevents overfitting. Powerful for both classification and regression.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:178,323

result = await ml_service.trainer.train_classifier(
    X=features,
    y=labels,
    algorithms=["random_forest"]
)

# How it works:
# 100 trees, each sees different subset of data and features
# Final prediction = majority vote (classification) or average (regression)

# Feature importance
importances = result['model'].feature_importances_
for feature, importance in zip(feature_names, importances):
    print(f"{feature}: {importance:.3f}")
```

**Use Cases:**
- Default choice for medium/large datasets
- High-dimensional data
- Robust predictions

**When to Use:**
✅ Medium to large datasets (1,000+)
✅ High dimensions (100+ features)
✅ Need robust model
✅ Want feature importance

**Hyperparameters:**
- **n_estimators=100:** Number of trees (higher = better but slower)
- **max_depth=None:** Tree depth (limit to prevent overfitting)

---

### 8. Gradient Boosting & XGBoost
**State-of-the-Art Ensemble**

**Theory from Overview:**
> Sequential ensemble where each model fixes errors of previous model. Combines weak models into strong model. XGBoost adds regularization and optimization.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/ml_service.py:183,327,332

# Gradient Boosting
result_gb = await ml_service.trainer.train_regressor(
    X=features,
    y=lpr_scores,
    algorithms=["gradient_boosting"]
)
# RMSE: 8.2

# XGBoost (better!)
result_xgb = await ml_service.trainer.train_regressor(
    X=features,
    y=lpr_scores,
    algorithms=["xgboost"]
)
# RMSE: 6.8 (17% improvement!)
```

**Use Cases:**
- Maximum accuracy needed
- Production systems
- Kaggle competitions (XGBoost often wins)

**When to Use:**
✅ Large datasets (5,000+)
✅ Need best accuracy
✅ Have computational resources
✅ Production deployment

**Gradient Boosting vs XGBoost:**
- **Gradient Boosting:** Good accuracy, standard library
- **XGBoost:** Better accuracy, faster, handles missing data, regularization

---

### 9. Neural Networks
**Deep Learning for Complex Patterns**

**Theory from Overview:**
> Automatically designs complex features without human guidance. Hidden layers represent unknown features. Deep learning = many layers (3+).

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/neural_network_service.py

from circuit_os_ml_service.intelligence.neural_network_service import NeuralNetworkService

nn_service = NeuralNetworkService()

# Multi-layer perceptron (3 hidden layers)
result = await nn_service.train_deep_classifier(
    X=features,
    y=labels,
    hidden_layers=(100, 50, 25)  # Layer sizes
)

# Architecture:
# Input (47 features)
#   ↓
# Hidden Layer 1 (100 neurons) - learns basic patterns
#   ↓
# Hidden Layer 2 (50 neurons) - combines into concepts
#   ↓
# Hidden Layer 3 (25 neurons) - high-level features
#   ↓
# Output (1 neuron) - final prediction
```

**Use Cases:**
- Email quality scoring
- Complex lead behavior patterns
- When other algorithms fail

**When to Use:**
✅ Large datasets (10,000+)
✅ Complex non-linear patterns
✅ Have GPU/computational resources
✅ Other algorithms plateau

**When NOT to Use:**
❌ Small datasets (will overfit)
❌ Need interpretability
❌ Limited compute resources

---

## 🔍 UNSUPERVISED LEARNING

### 10. K-Means Clustering
**Customer Segmentation**

**Theory from Overview:**
> Finds K clusters by: random centers → assign points → recalculate centers → repeat until stabilized.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/unsupervised_learning.py:40

from circuit_os_ml_service.intelligence.unsupervised_learning import UnsupervisedLearningService

unsupervised = UnsupervisedLearningService()

# Find optimal K
optimal_k = await unsupervised.find_optimal_clusters(X, max_k=10)
print(f"Recommended K: {optimal_k['recommended_k']}")

# Cluster leads
result = await unsupervised.kmeans_clustering(
    X=lead_features,
    n_clusters=5
)

clusters = result.clusters  # [0, 2, 1, 4, 3, ...]
"""
Cluster 0: High-Value Enterprise (847 leads)
Cluster 1: SMB Quick Closers (1234 leads)
Cluster 2: Tire Kickers (892 leads)
Cluster 3: Mid-Market Nurture (1456 leads)
Cluster 4: Churn Risk (571 leads)
"""
```

**Use Cases:**
- Customer segmentation
- Market research
- Personalized campaigns

**When to Use:**
✅ Discover hidden groups
✅ No labels available
✅ Know approximate number of segments

**Hyperparameters:**
- **n_clusters:** Number of segments (use silhouette score to find optimal)

---

### 11. Principal Component Analysis (PCA)
**Dimensionality Reduction**

**Theory from Overview:**
> Finds directions with most variance. Combines correlated features into principal components. Example: height + length → "shape" feature.

**Circuit OS Implementation:**
```python
# File: circuit_os_ml_service/intelligence/unsupervised_learning.py:125

# Problem: 47 features slow down training

result = await unsupervised.pca_reduction(
    X=features_47,
    n_components=5  # Reduce to 5 components
)

X_reduced = result.reduced_data  # (10000, 5)
variance = result.to_dict()['total_variance_explained']

print(f"Retained variance: {variance:.1%}")
# Output: "Retained variance: 92%" (47 → 5 features, kept 92% info!)

# Use reduced features for faster training
result = await ml_service.trainer.train_classifier(
    X=X_reduced,  # 5 features instead of 47
    y=labels
)
# Training time: 8x faster!
```

**Use Cases:**
- Feature reduction (47 → 5)
- Data visualization (reduce to 2D/3D)
- Remove correlated features
- Pre-processing step

**When to Use:**
✅ High dimensionality (50+ features)
✅ Slow training
✅ Visualization needed
✅ Features are correlated

---

## 🎯 ALGORITHM SELECTION GUIDE

### Quick Decision Tree

```
START: What's your goal?

├─ Predict NUMBER (LPR score, revenue)
│  ├─ Small data (< 500) → Linear Regression
│  ├─ Medium data (500-5K) → Gradient Boosting
│  └─ Large data (5K+) → XGBoost
│
├─ Predict CATEGORY (high/low intent, spam/not spam)
│  ├─ Text data → Naive Bayes
│  ├─ Need probabilities → Logistic Regression
│  ├─ Need interpretability → Decision Tree
│  ├─ Medium data → Random Forest
│  └─ Large data, max accuracy → XGBoost
│
├─ Find GROUPS (customer segments)
│  ├─ Know K → K-Means
│  ├─ Don't know K → DBSCAN
│  └─ Need hierarchy → Hierarchical Clustering
│
└─ Reduce FEATURES (47 → 5)
   └─ PCA
```

### Automated Selection

```python
from circuit_os_ml_service.intelligence.algorithm_selector import AlgorithmSelector

selector = AlgorithmSelector()

recommendation = selector.recommend_for_problem(
    problem_type="classification",
    n_samples=5000,
    n_features=47,
    interpretability_required=False
)

print(f"Use: {recommendation.algorithm}")
print(f"Because: {recommendation.reason}")
```

---

## 📊 EVALUATION METRICS

### Classification Metrics

**Accuracy:** Overall correctness
```python
accuracy = (true_positives + true_negatives) / total
# 85% accuracy = 85 out of 100 predictions correct
```

**Precision:** Of predicted positives, how many are correct?
```python
precision = true_positives / (true_positives + false_positives)
# 90% precision = 90% of "will convert" predictions were right
```

**Recall:** Of actual positives, how many did we find?
```python
recall = true_positives / (true_positives + false_negatives)
# 80% recall = found 80% of all converts
```

**F1 Score:** Harmonic mean of precision and recall (best overall metric)
```python
f1 = 2 * (precision * recall) / (precision + recall)
# Use F1 when you need balance between precision and recall
```

### Regression Metrics

**RMSE (Root Mean Squared Error):** Average prediction error
```python
rmse = sqrt(mean((y_true - y_pred) ** 2))
# RMSE = 8.2 means predictions within ±8.2 points on average
```

**MAE (Mean Absolute Error):** Average absolute error
```python
mae = mean(abs(y_true - y_pred))
# MAE = 6.3 means average error is 6.3 points
```

**R² (R-squared):** Variance explained
```python
r2 = 1 - (sum_squared_errors / total_variance)
# R² = 0.92 means model explains 92% of variance
```

---

## 🚀 PRODUCTION BEST PRACTICES

### 1. Start Simple, Then Optimize

```python
# Phase 1: Baseline (Linear/Logistic Regression)
baseline = await ml_service.trainer.train_classifier(
    X, y, algorithms=["logistic_regression"]
)

# Phase 2: Ensemble (Random Forest)
improved = await ml_service.trainer.train_classifier(
    X, y, algorithms=["random_forest"]
)

# Phase 3: State-of-the-art (XGBoost)
production = await ml_service.trainer.train_classifier(
    X, y, algorithms=["xgboost"]
)
```

### 2. A/B Test New Models

```python
# Gradual rollout
deployment = {
    "logistic_regression": 20%,  # Baseline
    "xgboost": 80%  # New model
}

# Monitor for 1 week, then deploy to 100%
```

### 3. Auto-Retrain on New Data

```python
# From ML-FEEDBACK-LOOP-SYSTEM.md

# After 50 outcomes, retrain
if len(outcomes) >= 50:
    await ml_service.auto_retrain(model_name)
```

### 4. Feature Engineering

See `FEATURE-ENGINEERING-GUIDE.md` for:
- Creating new features
- Handling missing data
- Feature scaling
- Feature selection

---

**Status:** ✅ Complete Algorithm Reference
**Integration:** All algorithms linked to Circuit OS code
**Next:** See `FEATURE-ENGINEERING-GUIDE.md` for feature design

---

**© 2025 CircuitOS™ - ML Reference Documentation**

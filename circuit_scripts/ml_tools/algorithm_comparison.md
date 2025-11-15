# Algorithm Comparison Tool
**Compare ALL ML Algorithms on Your Circuit OS Data**

## Purpose

Test all 10+ algorithms from the ML Algorithms Overview on your real Circuit OS data and find the best performer.

## Usage

```python
from circuit_os_ml_service.intelligence.ml_service import MLService
from circuit_os_ml_service.intelligence.algorithm_selector import AlgorithmSelector

ml_service = MLService()
selector = AlgorithmSelector()

# Load your data
X, y = load_your_data()

# Option 1: Let algorithm selector recommend
recommendation = selector.recommend_for_problem(
    problem_type="classification",  # or "regression"
    n_samples=len(X),
    n_features=X.shape[1],
    interpretability_required=False
)

print(f"Recommended: {recommendation.algorithm}")
print(f"Reason: {recommendation.reason}")

# Option 2: Test all algorithms
result = await ml_service.trainer.train_classifier(X, y)

print(f"\nBest Algorithm: {result['model_type']}")
print(f"Accuracy: {result['accuracy']:.1%}")
print(f"F1 Score: {result['f1_score']:.3f}")

# View all results
for algo, metrics in result['all_results'].items():
    print(f"{algo}: accuracy={metrics['accuracy']:.3f}, f1={metrics['f1_score']:.3f}")
```

## Example Output

### Classification Problem
```
Testing 12 classification algorithms on 5,000 leads...

Algorithm Performance:
├── logistic_regression: accuracy=0.842, f1=0.835, confidence=0.78
├── knn: accuracy=0.785, f1=0.771
├── naive_bayes: accuracy=0.861, f1=0.854
├── svm_linear: accuracy=0.856, f1=0.849
├── svm_rbf: accuracy=0.873, f1=0.867
├── svm_poly: accuracy=0.851, f1=0.843
├── decision_tree: accuracy=0.792, f1=0.785
├── random_forest: accuracy=0.887, f1=0.882
├── bagging: accuracy=0.879, f1=0.873
├── adaboost: accuracy=0.868, f1=0.861
├── gradient_boosting: accuracy=0.893, f1=0.889
└── xgboost: accuracy=0.912, f1=0.908 ← BEST

Winner: xgboost
Reason: Highest F1 score (0.908)
Improvement over baseline: +8.3% accuracy
```

### Regression Problem
```
Testing 9 regression algorithms on 10,000 leads...

Algorithm Performance:
├── linear_regression: RMSE=12.4, MAE=9.8, R²=0.76
├── knn: RMSE=11.2, MAE=8.9, R²=0.79
├── svr_linear: RMSE=11.8, MAE=9.3, R²=0.78
├── svr_rbf: RMSE=10.5, MAE=8.1, R²=0.82
├── decision_tree: RMSE=13.1, MAE=10.2, R²=0.74
├── random_forest: RMSE=9.7, MAE=7.5, R²=0.85
├── bagging: RMSE=10.1, MAE=7.9, R²=0.84
├── gradient_boosting: RMSE=8.2, MAE=6.3, R²=0.89
└── xgboost: RMSE=6.8, MAE=5.1, R²=0.92 ← BEST

Winner: xgboost
Reason: Lowest RMSE (6.8)
Improvement over baseline: 45.2% better predictions
```

## Comparison Criteria

### Classification
- **Accuracy:** Overall correctness
- **Precision:** How many predicted positives are correct
- **Recall:** How many actual positives were found
- **F1 Score:** Harmonic mean of precision and recall (best overall metric)
- **Confidence:** Average prediction confidence

### Regression
- **RMSE:** Root Mean Squared Error (lower is better)
- **MAE:** Mean Absolute Error (average prediction error)
- **R²:** Variance explained (closer to 1.0 is better)

## Automatic Recommendations

```python
# Get explanation for recommended algorithm
explanation = selector.explain_algorithm("xgboost")

print(explanation['theory'])
print(explanation['use_cases'])
print(explanation['when_to_use'])
```

## Production Deployment

```python
# After finding best algorithm, deploy it

# 1. Register best model
ml_service.registry.register(
    "lead_scorer_v3",
    result['model'],
    {
        "algorithm": result['model_type'],
        "accuracy": result['accuracy'],
        "trained_at": datetime.now(),
        "training_samples": len(X)
    }
)

# 2. Gradual rollout (A/B test)
deployment = {
    "lead_scorer_v2": 20%,  # Old model
    "lead_scorer_v3": 80%   # New XGBoost model
}

# 3. Monitor for 1 week
# 4. Deploy to 100% if performance improves
```

## Benchmarking Script

```python
import time

async def benchmark_all_algorithms(X, y, problem_type="classification"):
    """
    Comprehensive benchmark of all algorithms
    """
    results = []

    algorithms = [
        "logistic_regression", "knn", "naive_bayes", "svm_linear",
        "svm_rbf", "decision_tree", "random_forest", "gradient_boosting",
        "xgboost"
    ] if problem_type == "classification" else [
        "linear_regression", "knn", "svr_linear", "svr_rbf",
        "decision_tree", "random_forest", "gradient_boosting", "xgboost"
    ]

    for algo in algorithms:
        start_time = time.time()

        if problem_type == "classification":
            result = await ml_service.trainer.train_classifier(
                X, y, algorithms=[algo]
            )
            metric = result['f1_score']
        else:
            result = await ml_service.trainer.train_regressor(
                X, y, algorithms=[algo]
            )
            metric = result['rmse']

        training_time = time.time() - start_time

        results.append({
            "algorithm": algo,
            "metric": metric,
            "training_time": training_time,
            "samples": len(X)
        })

        print(f"{algo}: {metric:.3f} ({training_time:.2f}s)")

    return results
```

---

**© 2025 CircuitOS™ - ML Tools**

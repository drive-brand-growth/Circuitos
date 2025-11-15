"""
Algorithm Selector - Intelligent ML Algorithm Selection
From ML Algorithms Overview: "A simple strategy exists for picking the right algorithm"

Automatically recommends the best algorithm based on:
- Problem type (classification vs regression)
- Data size
- Feature count
- Data characteristics
- Performance requirements
"""

from typing import Dict, Any, List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


class AlgorithmRecommendation:
    """Recommendation for ML algorithm selection"""

    def __init__(
        self,
        algorithm: str,
        reason: str,
        overview_reference: str,
        alternatives: List[str] = None,
        confidence: float = 1.0
    ):
        self.algorithm = algorithm
        self.reason = reason
        self.overview_reference = overview_reference
        self.alternatives = alternatives or []
        self.confidence = confidence

    def to_dict(self) -> Dict:
        return {
            "algorithm": self.algorithm,
            "reason": self.reason,
            "overview_reference": self.overview_reference,
            "alternatives": self.alternatives,
            "confidence": self.confidence
        }


class AlgorithmSelector:
    """
    Intelligent algorithm selection based on ML Algorithms Overview principles

    Decision tree for algorithm selection:
    1. Classification vs Regression?
    2. Data size (small, medium, large)
    3. Feature count (low, medium, high dimensionality)
    4. Interpretability vs Accuracy tradeoff
    5. Training speed requirements
    """

    def __init__(self):
        self.recommendation_history = []

    def recommend_classifier(
        self,
        n_samples: int,
        n_features: int,
        interpretability_required: bool = False,
        text_data: bool = False,
        training_speed_critical: bool = False
    ) -> AlgorithmRecommendation:
        """
        Recommend classification algorithm

        From ML Algorithms Overview decision criteria:
        - Small data (< 1000): Simple algorithms to prevent overfitting
        - High dimensions (> 100 features): Algorithms that handle curse of dimensionality
        - Text data: Naive Bayes excels
        - Need interpretability: Decision trees, logistic regression
        - Need maximum accuracy: XGBoost, Random Forest
        """
        logger.info(
            f"Recommending classifier: {n_samples} samples, "
            f"{n_features} features, interpretability={interpretability_required}"
        )

        # Special case: Text classification
        if text_data:
            return AlgorithmRecommendation(
                algorithm="naive_bayes",
                reason=(
                    "Text classification - Naive Bayes is computationally efficient "
                    "and performs well on text by multiplying word probabilities"
                ),
                overview_reference="Naive Bayes: Fast, good for text-based tasks",
                alternatives=["logistic_regression", "svm_linear"],
                confidence=0.95
            )

        # Small dataset (< 1000 samples)
        if n_samples < 1000:
            if interpretability_required:
                return AlgorithmRecommendation(
                    algorithm="logistic_regression",
                    reason=(
                        f"Small dataset ({n_samples} samples) - Simple algorithm prevents overfitting. "
                        "Logistic regression provides interpretable probability scores and feature weights."
                    ),
                    overview_reference="Logistic Regression: Basic classification, probability scores",
                    alternatives=["decision_tree", "knn"],
                    confidence=0.90
                )
            else:
                return AlgorithmRecommendation(
                    algorithm="knn",
                    reason=(
                        f"Small dataset ({n_samples} samples) - KNN is non-parametric, "
                        "no model fitting required, works well with limited data"
                    ),
                    overview_reference="KNN: Non-parametric, no true model fitting necessary",
                    alternatives=["logistic_regression", "random_forest"],
                    confidence=0.85
                )

        # Medium dataset (1000-10,000 samples)
        if n_samples < 10000:
            # High dimensionality
            if n_features > 100:
                return AlgorithmRecommendation(
                    algorithm="random_forest",
                    reason=(
                        f"Medium dataset ({n_samples} samples) with high dimensionality "
                        f"({n_features} features) - Random Forest handles many features well, "
                        "prevents overfitting through random feature exclusion"
                    ),
                    overview_reference="Random Forest: Prevents overfitting, robust to high dimensions",
                    alternatives=["svm_rbf", "gradient_boosting"],
                    confidence=0.92
                )

            # Need interpretability
            if interpretability_required:
                return AlgorithmRecommendation(
                    algorithm="decision_tree",
                    reason=(
                        f"Medium dataset ({n_samples} samples) - Decision tree provides "
                        "clear yes/no rules that are easy to explain to stakeholders"
                    ),
                    overview_reference="Decision Tree: Interpretable rules, easy to visualize",
                    alternatives=["logistic_regression", "random_forest"],
                    confidence=0.88
                )

            # Need speed
            if training_speed_critical:
                return AlgorithmRecommendation(
                    algorithm="logistic_regression",
                    reason=(
                        f"Medium dataset ({n_samples} samples) - Logistic regression trains "
                        "very fast compared to ensemble methods"
                    ),
                    overview_reference="Logistic Regression: Fast training, good baseline",
                    alternatives=["naive_bayes", "knn"],
                    confidence=0.85
                )

            # General case: Maximize accuracy
            return AlgorithmRecommendation(
                algorithm="gradient_boosting",
                reason=(
                    f"Medium dataset ({n_samples} samples) - Gradient boosting achieves "
                    "high accuracy through sequential model improvement"
                ),
                overview_reference="Gradient Boosting: High accuracy, sequential improvement",
                alternatives=["random_forest", "svm_rbf"],
                confidence=0.90
            )

        # Large dataset (> 10,000 samples)
        if interpretability_required:
            return AlgorithmRecommendation(
                algorithm="logistic_regression",
                reason=(
                    f"Large dataset ({n_samples} samples) - Logistic regression scales well "
                    "and provides interpretable probability scores"
                ),
                overview_reference="Logistic Regression: Scalable, interpretable",
                alternatives=["decision_tree"],
                confidence=0.87
            )

        # Maximum accuracy on large dataset
        return AlgorithmRecommendation(
            algorithm="xgboost",
            reason=(
                f"Large dataset ({n_samples} samples) - XGBoost is state-of-the-art, "
                "optimized for speed and performance with regularization to prevent overfitting"
            ),
            overview_reference="XGBoost: State-of-the-art, optimized boosting",
            alternatives=["gradient_boosting", "random_forest"],
            confidence=0.95
        )

    def recommend_regressor(
        self,
        n_samples: int,
        n_features: int,
        interpretability_required: bool = False,
        training_speed_critical: bool = False
    ) -> AlgorithmRecommendation:
        """
        Recommend regression algorithm

        From ML Algorithms Overview:
        - Linear Regression: Mother of all ML, simple and interpretable
        - Gradient Boosting: High accuracy for complex patterns
        - XGBoost: State-of-the-art regression
        """
        logger.info(
            f"Recommending regressor: {n_samples} samples, "
            f"{n_features} features, interpretability={interpretability_required}"
        )

        # Small dataset (< 500 samples)
        if n_samples < 500:
            return AlgorithmRecommendation(
                algorithm="linear_regression",
                reason=(
                    f"Small dataset ({n_samples} samples) - Linear regression is the "
                    "mother of all ML algorithms, simple, interpretable, prevents overfitting"
                ),
                overview_reference="Linear Regression: Mother of all ML, minimizes sum of squares",
                alternatives=["knn", "decision_tree"],
                confidence=0.92
            )

        # Medium dataset (500-5,000 samples)
        if n_samples < 5000:
            if interpretability_required:
                return AlgorithmRecommendation(
                    algorithm="linear_regression",
                    reason=(
                        f"Medium dataset ({n_samples} samples) - Linear regression provides "
                        "clear feature coefficients showing impact of each variable"
                    ),
                    overview_reference="Linear Regression: Interpretable coefficients",
                    alternatives=["decision_tree"],
                    confidence=0.88
                )

            # High dimensionality
            if n_features > 50:
                return AlgorithmRecommendation(
                    algorithm="random_forest",
                    reason=(
                        f"Medium dataset ({n_samples} samples) with many features "
                        f"({n_features}) - Random Forest handles high dimensions well"
                    ),
                    overview_reference="Random Forest: Ensemble bagging for regression",
                    alternatives=["gradient_boosting"],
                    confidence=0.90
                )

            # General case
            return AlgorithmRecommendation(
                algorithm="gradient_boosting",
                reason=(
                    f"Medium dataset ({n_samples} samples) - Gradient boosting captures "
                    "complex non-linear patterns through sequential model improvement"
                ),
                overview_reference="Gradient Boosting: Sequential improvement, high accuracy",
                alternatives=["random_forest", "svr_rbf"],
                confidence=0.92
            )

        # Large dataset (> 5,000 samples)
        if interpretability_required:
            return AlgorithmRecommendation(
                algorithm="linear_regression",
                reason=(
                    f"Large dataset ({n_samples} samples) - Linear regression scales well "
                    "and provides interpretable results"
                ),
                overview_reference="Linear Regression: Scalable, interpretable",
                alternatives=["decision_tree"],
                confidence=0.85
            )

        # Maximum accuracy on large dataset
        return AlgorithmRecommendation(
            algorithm="xgboost",
            reason=(
                f"Large dataset ({n_samples} samples) - XGBoost achieves state-of-the-art "
                "regression performance with optimized gradient boosting"
            ),
            overview_reference="XGBoost: State-of-the-art regression",
            alternatives=["gradient_boosting", "random_forest"],
            confidence=0.95
        )

    def recommend_for_problem(
        self,
        problem_type: str,
        n_samples: int,
        n_features: int,
        **kwargs
    ) -> AlgorithmRecommendation:
        """
        Unified recommendation interface

        Args:
            problem_type: "classification" or "regression"
            n_samples: Number of training samples
            n_features: Number of features
            **kwargs: Additional parameters (interpretability_required, text_data, etc.)
        """
        if problem_type == "classification":
            recommendation = self.recommend_classifier(
                n_samples=n_samples,
                n_features=n_features,
                **kwargs
            )
        elif problem_type == "regression":
            recommendation = self.recommend_regressor(
                n_samples=n_samples,
                n_features=n_features,
                **kwargs
            )
        else:
            raise ValueError(f"Unknown problem_type: {problem_type}")

        # Store recommendation
        self.recommendation_history.append({
            "problem_type": problem_type,
            "n_samples": n_samples,
            "n_features": n_features,
            "recommendation": recommendation.to_dict(),
            **kwargs
        })

        return recommendation

    def explain_algorithm(self, algorithm_name: str) -> Dict[str, Any]:
        """
        Explain algorithm from ML Algorithms Overview

        Provides theory, use cases, and when to use each algorithm
        """
        explanations = {
            # Classification Algorithms
            "logistic_regression": {
                "type": "classification",
                "theory": (
                    "Variant of linear regression that fits a sigmoid function to predict "
                    "categorical output. Provides probability of data point falling into a class."
                ),
                "use_cases": [
                    "Binary classification (yes/no, spam/not spam)",
                    "When you need probability scores",
                    "Interpretable feature importance"
                ],
                "when_to_use": "Small to medium datasets, need interpretability and probabilities",
                "overview_section": "Logistic Regression"
            },

            "knn": {
                "type": "classification/regression",
                "theory": (
                    "Non-parametric algorithm that predicts based on K nearest neighbors. "
                    "Classification uses majority vote, regression uses average of neighbors."
                ),
                "use_cases": [
                    "Small datasets where model fitting is not needed",
                    "Lead similarity matching",
                    "Recommendation systems (find similar leads)"
                ],
                "when_to_use": "Small datasets, similarity-based predictions, no training required",
                "overview_section": "K-Nearest Neighbors (KNN)"
            },

            "svm_rbf": {
                "type": "classification/regression",
                "theory": (
                    "Finds decision boundary that maximizes margin between classes. "
                    "RBF kernel uses kernel trick to find complex non-linear patterns."
                ),
                "use_cases": [
                    "Complex pattern recognition",
                    "High-dimensional data",
                    "When linear separation is not possible"
                ],
                "when_to_use": "Medium datasets with complex non-linear patterns",
                "overview_section": "Support Vector Machine (SVM)"
            },

            "naive_bayes": {
                "type": "classification",
                "theory": (
                    "Based on Bayes' theorem, calculates probability by multiplying word occurrences. "
                    "Naive because assumes features are independent."
                ),
                "use_cases": [
                    "Text classification (spam filters)",
                    "Email intent classification",
                    "Fast predictions on text data"
                ],
                "when_to_use": "Text-based classification, need speed, limited data",
                "overview_section": "Naive Bayes Classifier"
            },

            "decision_tree": {
                "type": "classification/regression",
                "theory": (
                    "Series of yes/no questions that partition data into leaf nodes. "
                    "Goal is to create pure leaf nodes that minimize misclassification."
                ),
                "use_cases": [
                    "When interpretability is critical",
                    "Explaining decisions to stakeholders",
                    "Rule-based classification"
                ],
                "when_to_use": "Need interpretable rules, decision explanations required",
                "overview_section": "Decision Trees"
            },

            "random_forest": {
                "type": "classification/regression",
                "theory": (
                    "Ensemble of decision trees using bagging. Each tree votes on classification. "
                    "Random feature exclusion prevents overfitting."
                ),
                "use_cases": [
                    "High-dimensional data",
                    "When accuracy is important",
                    "Preventing overfitting"
                ],
                "when_to_use": "Medium to large datasets, high dimensions, need robust model",
                "overview_section": "Ensemble Algorithms - Bagging (Random Forest)"
            },

            "gradient_boosting": {
                "type": "classification/regression",
                "theory": (
                    "Sequential ensemble method where each model fixes errors of previous model. "
                    "Combines weak models into strong model."
                ),
                "use_cases": [
                    "Maximum accuracy needed",
                    "Complex patterns",
                    "LPR score prediction"
                ],
                "when_to_use": "Large datasets, need highest accuracy, training time not critical",
                "overview_section": "Ensemble Algorithms - Boosting"
            },

            "xgboost": {
                "type": "classification/regression",
                "theory": (
                    "Optimized gradient boosting with regularization. State-of-the-art performance "
                    "in machine learning competitions."
                ),
                "use_cases": [
                    "Kaggle competitions (often wins)",
                    "Maximum accuracy required",
                    "Large-scale production systems"
                ],
                "when_to_use": "Large datasets, need absolute best performance, have computational resources",
                "overview_section": "Ensemble Algorithms - XGBoost"
            },

            # Regression Algorithms
            "linear_regression": {
                "type": "regression",
                "theory": (
                    "Mother of all ML algorithms. Finds linear relationship between input and output "
                    "by minimizing sum of squares of distances."
                ),
                "use_cases": [
                    "LPR score prediction",
                    "Revenue forecasting",
                    "Feature importance analysis"
                ],
                "when_to_use": "Small datasets, linear relationships, need interpretability",
                "overview_section": "Linear Regression"
            },

            # Unsupervised Algorithms
            "kmeans": {
                "type": "clustering",
                "theory": (
                    "Finds K clusters by: random centers → assign points → recalculate centers → repeat. "
                    "Stops when centers stabilize."
                ),
                "use_cases": [
                    "Customer segmentation",
                    "Market segment discovery",
                    "Lead grouping by behavior"
                ],
                "when_to_use": "Need to discover groups in data, know number of clusters",
                "overview_section": "K-Means Clustering"
            },

            "pca": {
                "type": "dimensionality_reduction",
                "theory": (
                    "Finds directions with most variance in data. Combines correlated features "
                    "into principal components."
                ),
                "use_cases": [
                    "Feature reduction (47 → 5 features)",
                    "Data visualization (reduce to 2D/3D)",
                    "Remove correlated features"
                ],
                "when_to_use": "High-dimensional data, feature reduction needed, pre-processing step",
                "overview_section": "Principal Component Analysis (PCA)"
            }
        }

        return explanations.get(algorithm_name, {
            "error": f"Algorithm {algorithm_name} not found in explanations"
        })

    def get_metrics(self) -> Dict[str, Any]:
        """Get algorithm selector metrics"""
        return {
            "total_recommendations": len(self.recommendation_history),
            "recent_recommendations": self.recommendation_history[-10:]
        }

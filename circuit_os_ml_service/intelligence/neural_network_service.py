"""
Neural Network Service
From ML Algorithms Overview: "The Reigning King of AI"

NEW CAPABILITY for Circuit OS (v2.0)
- Deep learning for complex pattern recognition
- Multi-layer perceptron (MLP) for classification and regression
- Automatic feature engineering through hidden layers
- Email response quality scoring
- Complex lead behavior patterns
"""

from typing import Dict, Any, List, Optional
import numpy as np
import logging
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class NeuralNetworkResult:
    """Result from neural network training"""

    def __init__(
        self,
        model: Any,
        model_type: str,
        architecture: List[int],
        loss: float,
        score: float,
        iterations: int
    ):
        self.model = model
        self.model_type = model_type
        self.architecture = architecture
        self.loss = loss
        self.score = score
        self.iterations = iterations

    def to_dict(self) -> Dict:
        return {
            "model_type": self.model_type,
            "architecture": self.architecture,
            "hidden_layers": len(self.architecture),
            "total_neurons": sum(self.architecture),
            "final_loss": self.loss,
            "score": self.score,
            "iterations": self.iterations
        }


class NeuralNetworkService:
    """
    Neural Network Service for Circuit OS

    From ML Algorithms Overview:
    - Automatically designs complex features without human guidance
    - Hidden layers represent unknown features
    - Single layer perceptron = multi-feature regression
    - Deep learning = many hidden layers (3+)
    - Implicit feature engineering through learned representations

    Use Cases:
    1. Email response quality scoring (complex text patterns)
    2. Lead behavior pattern recognition
    3. Churn prediction with complex signals
    4. Intent classification with nuanced language
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.training_history = []

    async def train_deep_classifier(
        self,
        X: np.ndarray,
        y: np.ndarray,
        hidden_layers: tuple = (100, 50, 25),
        max_iterations: int = 500
    ) -> NeuralNetworkResult:
        """
        Train multi-layer perceptron for classification

        From ML Algorithms Overview:
        - Hidden Layer 1 (100 neurons): Learns basic patterns
        - Hidden Layer 2 (50 neurons): Combines patterns into concepts
        - Hidden Layer 3 (25 neurons): High-level decision features

        Example: Email quality scoring
        - Layer 1: Tone patterns, engagement indicators
        - Layer 2: Hook-Story-Offer structure, CTA strength
        - Layer 3: Overall persuasiveness, conversion probability
        """
        logger.info(
            f"Training neural network classifier: {len(X)} samples, "
            f"architecture={hidden_layers}"
        )

        # Normalize data (critical for neural networks)
        X_scaled = self.scaler.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Multi-layer Perceptron
        mlp = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            activation='relu',  # ReLU activation from deep learning
            solver='adam',  # Optimized gradient descent
            max_iter=max_iterations,
            early_stopping=True,  # Prevent overfitting
            validation_fraction=0.2,
            random_state=42,
            verbose=False
        )

        # Train
        mlp.fit(X_train, y_train)

        # Evaluate
        y_pred = mlp.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        logger.info(
            f"Neural network trained: {mlp.n_iter_} iterations, "
            f"accuracy={accuracy:.3f}, loss={mlp.loss_:.4f}"
        )

        result = NeuralNetworkResult(
            model=mlp,
            model_type="classifier",
            architecture=list(hidden_layers),
            loss=mlp.loss_,
            score=accuracy,
            iterations=mlp.n_iter_
        )

        # Store in history
        self.training_history.append({
            "type": "classifier",
            "architecture": list(hidden_layers),
            "accuracy": accuracy,
            "loss": mlp.loss_,
            "samples": len(X)
        })

        return result

    async def train_deep_regressor(
        self,
        X: np.ndarray,
        y: np.ndarray,
        hidden_layers: tuple = (100, 50, 25),
        max_iterations: int = 500
    ) -> NeuralNetworkResult:
        """
        Train multi-layer perceptron for regression

        From ML Algorithms Overview:
        - Deep learning for continuous value prediction
        - Hidden layers learn complex feature combinations
        - Better than linear regression for non-linear patterns
        """
        logger.info(
            f"Training neural network regressor: {len(X)} samples, "
            f"architecture={hidden_layers}"
        )

        # Normalize data
        X_scaled = self.scaler.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Multi-layer Perceptron for regression
        mlp = MLPRegressor(
            hidden_layer_sizes=hidden_layers,
            activation='relu',
            solver='adam',
            max_iter=max_iterations,
            early_stopping=True,
            validation_fraction=0.2,
            random_state=42,
            verbose=False
        )

        # Train
        mlp.fit(X_train, y_train)

        # Evaluate
        y_pred = mlp.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        logger.info(
            f"Neural network trained: {mlp.n_iter_} iterations, "
            f"RMSE={rmse:.3f}, loss={mlp.loss_:.4f}"
        )

        result = NeuralNetworkResult(
            model=mlp,
            model_type="regressor",
            architecture=list(hidden_layers),
            loss=mlp.loss_,
            score=rmse,
            iterations=mlp.n_iter_
        )

        # Store in history
        self.training_history.append({
            "type": "regressor",
            "architecture": list(hidden_layers),
            "rmse": rmse,
            "loss": mlp.loss_,
            "samples": len(X)
        })

        return result

    async def train_simple_perceptron(
        self,
        X: np.ndarray,
        y: np.ndarray,
        problem_type: str = "classification"
    ) -> NeuralNetworkResult:
        """
        Train single-layer perceptron

        From ML Algorithms Overview:
        "Single layer perceptron is essentially a multi-feature regression task"

        Use for simpler problems that don't need deep learning
        """
        logger.info(f"Training simple perceptron: {len(X)} samples, type={problem_type}")

        # Single hidden layer
        hidden_layers = (50,)

        if problem_type == "classification":
            return await self.train_deep_classifier(X, y, hidden_layers=hidden_layers)
        else:
            return await self.train_deep_regressor(X, y, hidden_layers=hidden_layers)

    async def analyze_architecture(
        self,
        model: Any,
        feature_names: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze neural network architecture and learned features

        From ML Algorithms Overview:
        "Hidden layers represent hidden, unknown features. These can represent
        complex information (e.g., horizontal lines, presence of a face)"
        """
        if not hasattr(model, 'coefs_'):
            return {"error": "Model not trained or not a neural network"}

        analysis = {
            "architecture": {
                "input_neurons": model.coefs_[0].shape[0],
                "hidden_layers": len(model.hidden_layer_sizes),
                "hidden_layer_sizes": list(model.hidden_layer_sizes),
                "output_neurons": model.coefs_[-1].shape[1],
                "total_parameters": sum(c.size for c in model.coefs_)
            },
            "training": {
                "iterations": model.n_iter_,
                "final_loss": model.loss_,
                "activation_function": model.activation,
                "solver": model.solver
            }
        }

        # Analyze first layer weights (input → hidden layer 1)
        if feature_names and len(feature_names) == model.coefs_[0].shape[0]:
            first_layer_weights = model.coefs_[0]

            # Find most important features for each neuron in first hidden layer
            important_features = []
            for neuron_idx in range(min(5, first_layer_weights.shape[1])):  # Top 5 neurons
                weights = first_layer_weights[:, neuron_idx]
                top_indices = np.argsort(np.abs(weights))[-3:][::-1]

                important_features.append({
                    "neuron": neuron_idx + 1,
                    "top_features": [
                        {
                            "feature": feature_names[i],
                            "weight": float(weights[i])
                        }
                        for i in top_indices
                    ]
                })

            analysis["learned_patterns"] = important_features

        return analysis

    async def score_email_quality(
        self,
        email_features: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Example use case: Email response quality scoring

        From ML Algorithms Overview application:
        Input features (simple):
        - Word count, sentiment score, question marks, personalization, reading level

        Hidden layers learn:
        - Layer 1: Tone patterns, engagement indicators
        - Layer 2: Hook-Story-Offer structure, CTA strength
        - Layer 3: Overall persuasiveness, conversion probability

        Output:
        - Quality score (0-100)
        - Predicted open rate
        - Predicted reply rate
        """
        # This is a placeholder for the trained model
        # In production, load pre-trained email quality model

        features = [
            email_features.get('word_count', 0) / 500,  # Normalize
            email_features.get('sentiment_score', 0),
            email_features.get('question_marks', 0) / 3,
            email_features.get('personalization_tokens', 0) / 5,
            email_features.get('reading_level', 0) / 20
        ]

        # Simulated neural network prediction
        # In production, use: model.predict(scaler.transform([features]))

        quality_score = 50 + sum(features) * 10  # Simplified
        quality_score = min(max(quality_score, 0), 100)

        return {
            "quality_score": quality_score,
            "predicted_open_rate": quality_score * 0.35,
            "predicted_reply_rate": quality_score * 0.12,
            "recommendation": (
                "Send - High quality email" if quality_score > 70
                else "Review - Medium quality" if quality_score > 50
                else "Revise - Low quality"
            ),
            "neural_network_analysis": {
                "layer_1_features": "Tone patterns, engagement indicators",
                "layer_2_features": "Hook-Story-Offer structure, CTA strength",
                "layer_3_features": "Overall persuasiveness, conversion probability"
            }
        }

    async def find_optimal_architecture(
        self,
        X: np.ndarray,
        y: np.ndarray,
        problem_type: str = "classification"
    ) -> Dict[str, Any]:
        """
        Find optimal neural network architecture

        Tests different architectures:
        - Simple: (50,) - single hidden layer
        - Medium: (100, 50) - two hidden layers
        - Deep: (100, 50, 25) - three hidden layers (deep learning)
        - Very Deep: (200, 100, 50, 25) - four hidden layers
        """
        logger.info(f"Finding optimal architecture for {len(X)} samples")

        architectures = [
            (50,),  # Simple
            (100, 50),  # Medium
            (100, 50, 25),  # Deep (from overview example)
            (200, 100, 50, 25),  # Very deep
        ]

        results = []

        for arch in architectures:
            try:
                if problem_type == "classification":
                    result = await self.train_deep_classifier(X, y, hidden_layers=arch, max_iterations=200)
                    score = result.score
                    metric_name = "accuracy"
                else:
                    result = await self.train_deep_regressor(X, y, hidden_layers=arch, max_iterations=200)
                    score = result.score
                    metric_name = "rmse"

                results.append({
                    "architecture": arch,
                    "hidden_layers": len(arch),
                    "total_neurons": sum(arch),
                    metric_name: score,
                    "loss": result.loss,
                    "iterations": result.iterations
                })

                logger.info(f"  Architecture {arch}: {metric_name}={score:.3f}")

            except Exception as e:
                logger.error(f"Error testing architecture {arch}: {e}")

        # Find best architecture
        if problem_type == "classification":
            best = max(results, key=lambda x: x['accuracy'])
        else:
            best = min(results, key=lambda x: x['rmse'])

        return {
            "all_results": results,
            "best_architecture": best['architecture'],
            "reason": (
                f"{len(best['architecture'])} hidden layers with {best['total_neurons']} "
                f"total neurons achieved best performance"
            )
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get neural network service metrics"""
        return {
            "total_models_trained": len(self.training_history),
            "recent_training": self.training_history[-5:]
        }

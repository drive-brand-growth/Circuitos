"""
ML Service - Machine Learning with AutoML
Self-improving models with feedback loops
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import numpy as np
import pickle
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib

logger = logging.getLogger(__name__)


class Prediction:
    """ML prediction result"""

    def __init__(
        self,
        score: float,
        confidence: float,
        feature_importance: Dict[str, float] = None,
        model_version: str = "1.0"
    ):
        self.score = score
        self.confidence = confidence
        self.feature_importance = feature_importance or {}
        self.model_version = model_version

    def to_dict(self) -> Dict:
        return {
            "score": self.score,
            "confidence": self.confidence,
            "feature_importance": self.feature_importance,
            "model_version": self.model_version
        }


class ModelRegistry:
    """
    Registry for managing ML models
    """

    def __init__(self):
        self.models = {}
        self.metadata = {}

    def register(
        self,
        name: str,
        model: Any,
        metadata: Dict[str, Any] = None
    ):
        """Register a model"""
        self.models[name] = model
        self.metadata[name] = metadata or {}
        self.metadata[name]['registered_at'] = datetime.now().isoformat()
        logger.info(f"Registered model: {name}")

    def get(self, name: str) -> Optional[Any]:
        """Get a model"""
        return self.models.get(name)

    def list(self) -> List[str]:
        """List all models"""
        return list(self.models.keys())

    def get_metadata(self, name: str) -> Dict:
        """Get model metadata"""
        return self.metadata.get(name, {})


class AutoMLTrainer:
    """
    AutoML training with model selection and hyperparameter tuning
    """

    def __init__(self):
        self.training_history = []

    async def train_classifier(
        self,
        X: np.ndarray,
        y: np.ndarray,
        model_name: str = "auto_classifier"
    ) -> Dict[str, Any]:
        """
        Train classification model with auto model selection
        """
        logger.info(f"Training classifier {model_name} with {len(X)} samples")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Try different models
        models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
        }

        best_model = None
        best_accuracy = 0
        best_model_name = None

        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)

                logger.info(f"  {name}: accuracy={accuracy:.3f}")

                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = model
                    best_model_name = name

            except Exception as e:
                logger.error(f"Error training {name}: {e}")

        training_result = {
            "model": best_model,
            "model_type": best_model_name,
            "accuracy": best_accuracy,
            "samples": len(X),
            "trained_at": datetime.now().isoformat()
        }

        self.training_history.append(training_result)
        return training_result

    async def train_regressor(
        self,
        X: np.ndarray,
        y: np.ndarray,
        model_name: str = "auto_regressor"
    ) -> Dict[str, Any]:
        """
        Train regression model
        """
        logger.info(f"Training regressor {model_name} with {len(X)} samples")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        logger.info(f"  RMSE: {rmse:.3f}")

        training_result = {
            "model": model,
            "model_type": "gradient_boosting",
            "rmse": rmse,
            "samples": len(X),
            "trained_at": datetime.now().isoformat()
        }

        self.training_history.append(training_result)
        return training_result


class MLService:
    """
    ML Service with inference and AutoML training
    """

    def __init__(self):
        self.registry = ModelRegistry()
        self.trainer = AutoMLTrainer()
        self.prediction_history = []  # For feedback loops
        self.outcome_tracking = []

        # Initialize with default models
        self._initialize_default_models()

    def _initialize_default_models(self):
        """Initialize with default pre-trained models (simulated)"""
        # Lead scoring model (simulated)
        logger.info("Initializing default models...")

        # Register a simple lead scoring function as a "model"
        self.registry.register(
            "lead_scorer_v2",
            self._default_lead_scorer,
            {"type": "lead_scoring", "version": "2.0"}
        )

        # Churn prediction model
        self.registry.register(
            "churn_predictor_v1",
            self._default_churn_predictor,
            {"type": "churn_prediction", "version": "1.0"}
        )

    def _default_lead_scorer(self, features: Dict) -> Prediction:
        """Default lead scoring logic"""
        score = 50.0  # Base score

        # Engagement
        score += features.get("engagement_score", 0) * 0.35

        # Company size
        company_size = features.get("company_size", 0)
        if company_size > 100:
            score += 15
        elif company_size > 50:
            score += 10

        # Industry
        if features.get("industry") in ["Technology", "SaaS", "Finance"]:
            score += 10

        # Geographic fit
        score += features.get("geographic_fit", 0) * 15

        # Website traffic
        traffic = features.get("website_traffic", 0)
        if traffic > 100000:
            score += 10
        elif traffic > 50000:
            score += 5

        # Clamp to 0-100
        score = min(max(score, 0), 100)

        # Calculate confidence based on feature completeness
        feature_count = sum(1 for v in features.values() if v)
        confidence = min(0.5 + (feature_count * 0.1), 0.95)

        feature_importance = {
            "engagement_score": 0.35,
            "company_size": 0.25,
            "geographic_fit": 0.20,
            "industry": 0.15,
            "website_traffic": 0.05
        }

        return Prediction(
            score=score,
            confidence=confidence,
            feature_importance=feature_importance
        )

    def _default_churn_predictor(self, features: Dict) -> Prediction:
        """Default churn prediction logic"""
        churn_risk = 0.0

        # Usage decline
        if features.get("usage_decline", 0) > 0.5:
            churn_risk += 0.4

        # Support tickets
        if features.get("support_tickets", 0) > 5:
            churn_risk += 0.25

        # Payment delays
        if features.get("payment_delays", 0) > 0:
            churn_risk += 0.20

        # Engagement drop
        if features.get("engagement_drop", 0) > 0.3:
            churn_risk += 0.15

        churn_risk = min(churn_risk, 1.0)

        return Prediction(
            score=churn_risk,
            confidence=0.75,
            feature_importance={
                "usage_decline": 0.40,
                "support_tickets": 0.25,
                "payment_delays": 0.20,
                "engagement_drop": 0.15
            }
        )

    async def predict(
        self,
        model_name: str,
        features: Dict[str, Any]
    ) -> Prediction:
        """
        Get ML prediction
        """
        model = self.registry.get(model_name)

        if model is None:
            logger.error(f"Model {model_name} not found")
            return Prediction(score=0, confidence=0)

        # If model is callable (function), call it
        if callable(model):
            prediction = model(features)
        else:
            # If it's a scikit-learn model, use it
            try:
                # Convert features to array (would need proper feature engineering in production)
                X = np.array([[features.get(k, 0) for k in sorted(features.keys())]])
                score = model.predict(X)[0]
                confidence = 0.8  # Would use model.predict_proba in production

                prediction = Prediction(
                    score=float(score),
                    confidence=confidence
                )
            except Exception as e:
                logger.error(f"Error during prediction: {e}")
                return Prediction(score=0, confidence=0)

        # Track prediction for feedback loop
        prediction_record = {
            "model_name": model_name,
            "features": features,
            "prediction": prediction.to_dict(),
            "timestamp": datetime.now().isoformat(),
            "outcome_tracked": False
        }
        self.prediction_history.append(prediction_record)

        logger.info(f"Prediction from {model_name}: score={prediction.score:.2f}, confidence={prediction.confidence:.2f}")

        return prediction

    async def record_outcome(
        self,
        model_name: str,
        features: Dict[str, Any],
        actual_outcome: bool,
        outcome_value: float = 0.0
    ):
        """
        Record actual outcome for model improvement
        """
        outcome_record = {
            "model_name": model_name,
            "features": features,
            "actual_outcome": actual_outcome,
            "outcome_value": outcome_value,
            "timestamp": datetime.now().isoformat()
        }

        self.outcome_tracking.append(outcome_record)

        logger.info(f"Recorded outcome for {model_name}: {actual_outcome}")

        # Check if we should retrain
        outcomes_for_model = [
            o for o in self.outcome_tracking
            if o['model_name'] == model_name
        ]

        if len(outcomes_for_model) >= 50:  # Threshold for retraining
            logger.info(f"Threshold reached for {model_name}, triggering retrain")
            await self.auto_retrain(model_name)

    async def auto_retrain(self, model_name: str):
        """
        Automatically retrain model with new data
        """
        logger.info(f"Auto-retraining {model_name}...")

        # Get outcomes for this model
        outcomes = [
            o for o in self.outcome_tracking
            if o['model_name'] == model_name
        ]

        if len(outcomes) < 10:
            logger.warning(f"Not enough data to retrain {model_name}")
            return

        # Prepare training data
        X = []
        y = []

        for outcome in outcomes:
            features = outcome['features']
            # Convert features to array (simplified)
            feature_vector = [
                features.get('engagement_score', 0),
                features.get('company_size', 0),
                features.get('geographic_fit', 0),
                features.get('website_traffic', 0)
            ]
            X.append(feature_vector)
            y.append(1 if outcome['actual_outcome'] else 0)

        X = np.array(X)
        y = np.array(y)

        # Train new model
        result = await self.trainer.train_classifier(X, y, model_name)

        # Register new model if better
        old_metadata = self.registry.get_metadata(model_name)
        if result['accuracy'] > old_metadata.get('accuracy', 0):
            logger.info(f"New model is better! Deploying {model_name} v{result['model_type']}")
            self.registry.register(
                model_name,
                result['model'],
                {
                    **result,
                    'previous_accuracy': old_metadata.get('accuracy', 0),
                    'improvement': result['accuracy'] - old_metadata.get('accuracy', 0)
                }
            )
        else:
            logger.info(f"New model not better, keeping existing {model_name}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get ML service metrics"""
        return {
            "total_predictions": len(self.prediction_history),
            "total_outcomes": len(self.outcome_tracking),
            "models_registered": len(self.registry.list()),
            "models": {
                name: self.registry.get_metadata(name)
                for name in self.registry.list()
            },
            "training_history": len(self.trainer.training_history)
        }

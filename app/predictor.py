import os
import joblib
import numpy as np
import logging
from app.config import MODEL_PATH, VECTORIZER_PATH
from app.preprocess import preprocess_text

logger = logging.getLogger("app")

class SentimentPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def load_model(self):
        """
        Loads the model and vectorizer artifacts.
        Guarantees that loading occurs only once.
        """
        if self.model is not None and self.vectorizer is not None:
            return

        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model file not found at: {MODEL_PATH}")
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
        
        if not os.path.exists(VECTORIZER_PATH):
            logger.error(f"Vectorizer file not found at: {VECTORIZER_PATH}")
            raise FileNotFoundError(f"Vectorizer file not found at: {VECTORIZER_PATH}")

        logger.info(f"Loading serialized model from: {MODEL_PATH}")
        self.model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully.")
        
        logger.info(f"Loading serialized vectorizer from: {VECTORIZER_PATH}")
        self.vectorizer = joblib.load(VECTORIZER_PATH)
        logger.info("Vectorizer loaded successfully.")

    def predict(self, raw_text: str) -> dict:
        """
        Cleans, vectorizes, and predicts the sentiment of a raw tweet string.
        Estimates the confidence score depending on the model's available decision APIs.
        """
        if self.model is None or self.vectorizer is None:
            self.load_model()
            
        # 1. Clean the text using the exact training preprocessing
        cleaned_text = preprocess_text(raw_text)
        
        # Edge case: If preprocessing leaves the string empty
        if not cleaned_text.strip():
            logger.warning(f"Tweet preprocessed to empty string. Input: '{raw_text}'")
            return {
                "prediction": "Negative",
                "confidence_score": 0.50
            }
            
        # 2. Extract features using fitted TF-IDF
        vectorized_text = self.vectorizer.transform([cleaned_text])
        
        # 3. Classify sentiment (0 = Negative, 1 = Positive)
        prediction_class = int(self.model.predict(vectorized_text)[0])
        prediction_label = "Positive" if prediction_class == 1 else "Negative"
        
        # 4. Estimate confidence score
        # CODE COMMENT: LinearSVC does not support predict_proba() directly as it is a non-probabilistic
        # geometric classifier. We estimate a confidence score by passing the distance from the decision boundary
        # (decision_function) through a Sigmoid activation function. This is an estimated score, not a true calibrated probability.
        if hasattr(self.model, "decision_function"):
            decision_val = self.model.decision_function(vectorized_text)[0]
            probability = 1.0 / (1.0 + np.exp(-decision_val))
            
            if prediction_class == 1:
                confidence_score = float(probability)
            else:
                confidence_score = float(1.0 - probability)
        elif hasattr(self.model, "predict_proba"):
            # Fallback if a probabilistic model (like Logistic Regression) is loaded
            probabilities = self.model.predict_proba(vectorized_text)[0]
            confidence_score = float(probabilities[prediction_class])
        else:
            # Fallback if neither is available
            confidence_score = 1.0
            
        # Round confidence score to two decimal places
        confidence_score = round(confidence_score, 2)
        
        return {
            "prediction": prediction_label,
            "confidence_score": confidence_score
        }

# Create a singleton instance to be shared across requests
predictor = SentimentPredictor()

import joblib
import os
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from detector import PhishingDetector


def test_predict_with_saved_model(tmp_path):
    """Ensure the detector can load a saved model and make a prediction."""

    # Create a simple TF-IDF vectorizer + dummy classifier
    texts = ["hello world", "urgent action required"]
    labels = [0, 1]

    vectorizer = TfidfVectorizer()
    vectorized = vectorizer.fit_transform(texts)

    clf = DummyClassifier(strategy="constant", constant=1)
    clf.fit(vectorized, labels)

    model_path = tmp_path / "test_model.pkl"
    vectorizer_path = tmp_path / "test_vectorizer.pkl"

    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    detector = PhishingDetector(model_path=str(model_path), vectorizer_path=str(vectorizer_path))
    result = detector.predict("Hello", "Please confirm your account")

    assert result["prediction"] == "phishing"
    assert 0.0 <= result["confidence"] <= 1.0
    assert "threat_score" in result


def test_predict_without_model_files(tmp_path):
    """Detector should return 'unknown' prediction if model files are missing."""

    missing_model = tmp_path / "missing_model.pkl"
    missing_vectorizer = tmp_path / "missing_vectorizer.pkl"

    detector = PhishingDetector(model_path=str(missing_model), vectorizer_path=str(missing_vectorizer))
    result = detector.predict("Hello", "World")

    assert result["prediction"] == "unknown"
    assert result["confidence"] == 0.0
    assert result["risk_level"] == "high"

import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class PhishingDetector:
    def __init__(self, model_path='phishing_model.pkl', vectorizer_path='vectorizer.pkl'):
        """Initialize the phishing detector with trained model"""
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and vectorizer"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
            else:
                print(f"Model or vectorizer not found. Please train the model first.")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict(self, email_subject, email_body):
        """
        Predict if an email is phishing or legitimate
        
        Args:
            email_subject (str): Subject of the email
            email_body (str): Body of the email
        
        Returns:
            dict: Contains prediction, confidence, and risk_level
        """
        if self.model is None or self.vectorizer is None:
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'risk_level': 'high',
                'message': 'Model not loaded. Please train the model first.'
            }
        
        # Combine subject and body
        email_text = f"{email_subject} {email_body}"
        
        try:
            # Vectorize the text
            email_vec = self.vectorizer.transform([email_text])
            
            # Make prediction
            prediction = self.model.predict(email_vec)[0]
            confidence = max(self.model.predict_proba(email_vec)[0])
            
            # Determine risk level
            if prediction == 1:  # Phishing
                risk_level = 'high' if confidence > 0.8 else 'medium'
                prediction_label = 'phishing'
            else:  # Legitimate
                risk_level = 'low'
                prediction_label = 'legitimate'

            # simple threat score (0-100) and recommendations
            threat_score = round(confidence * 100, 2)
            recommendations = []
            if prediction_label == 'phishing':
                recommendations.append('Do not click any links or download attachments.')
                if risk_level == 'high':
                    recommendations.append('Report this email to your security team immediately.')
            else:
                recommendations.append('Email appears safe, but always verify sender.');

            return {
                'prediction': prediction_label,
                'confidence': float(confidence),
                'risk_level': risk_level,
                'threat_score': threat_score,
                'recommendations': recommendations
            }
        except Exception as e:
            return {
                'prediction': 'error',
                'confidence': 0.0,
                'risk_level': 'unknown',
                'message': str(e)
            }

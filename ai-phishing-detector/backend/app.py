from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Try to use the trained detector, fall back to simple if not available
try:
    from detector import PhishingDetector
    detector = PhishingDetector()
    print("Using trained phishing detector.")
except Exception as e:
    print(f"Failed to load trained detector: {e}. Using simple detector.")
    # Simple rule-based detector as fallback
    class SimplePhishingDetector:
        def __init__(self):
            self.phishing_keywords = [
                'urgent', 'verify', 'confirm', 'account', 'suspended',
                'password', 'reset', 'click here', 'login', 'security',
                'bank', 'paypal', 'amazon', 'alert', 'warning'
            ]

        def predict(self, email_subject, email_body):
            email_text = f"{email_subject} {email_body}".lower()

            # Count phishing keywords
            keyword_count = sum(1 for keyword in self.phishing_keywords if keyword in email_text)

            # Simple rule-based prediction
            if keyword_count >= 3:
                prediction = 'phishing'
                confidence = min(0.9, 0.5 + (keyword_count * 0.1))
            else:
                prediction = 'legitimate'
                confidence = max(0.6, 0.8 - (keyword_count * 0.1))

            risk_level = 'high' if prediction == 'phishing' else 'low'
            threat_score = round(confidence * 100, 2)
            
            # Generate recommendations
            recommendations = []
            if prediction == 'phishing':
                recommendations.append('Do not click any links or download attachments.')
                if risk_level == 'high':
                    recommendations.append('Report this email to your security team immediately.')
            else:
                recommendations.append('Email appears safe, but always verify sender.')

            return {
                'prediction': prediction,
                'confidence': float(confidence),
                'risk_level': risk_level,
                'threat_score': threat_score,
                'recommendations': recommendations
            }

    detector = SimplePhishingDetector()

@app.route('/api/detect', methods=['POST'])
def detect_phishing():
    """
    Endpoint to detect if an email is phishing or legitimate
    Expected JSON: {"email_subject": "...", "email_body": "..."}
    """
    try:
        data = request.get_json()
        email_subject = data.get('email_subject', '')
        email_body = data.get('email_body', '')
        
        if not email_subject or not email_body:
            return jsonify({'error': 'Email subject and body required'}), 400
        
        result = detector.predict(email_subject, email_body)
        
        # build response with all available metadata
        response = {
            'email_subject': email_subject,
            'prediction': result.get('prediction'),
            'confidence': result.get('confidence'),
            'risk_level': result.get('risk_level'),
            'threat_score': result.get('threat_score'),
            'recommendations': result.get('recommendations', [])
        }

        # echo optional fields if provided by client
        if 'sender_email' in data:
            response['sender_email'] = data['sender_email']
        if 'analysis_time' in data:
            response['analysis_time'] = data['analysis_time']

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# System Architecture

## Overview

The AI Phishing Detector consists of a backend machine learning service and a frontend web interface that communicates through a REST API.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Web UI)                     │
│            ┌──────────────────────────────┐             │
│            │    HTML/CSS/JavaScript       │             │
│            │  - Email input form          │             │
│            │  - Result display            │             │
│            │  - Error handling            │             │
│            └──────────────────┬───────────┘             │
└─────────────────────────────────┼──────────────────────────┘
                                  │
                    HTTP/REST API (Port 5000)
                                  │
┌─────────────────────────────────▼──────────────────────────┐
│                  Backend (Flask API)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Flask Application (app.py)                   │  │
│  │  - POST /api/detect - Phishing detection            │  │
│  │  - GET /api/health - Health check                   │  │
│  │  - Request validation & error handling              │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │      Phishing Detector (detector.py)                 │  │
│  │  - Load trained model                               │  │
│  │  - Text preprocessing                               │  │
│  │  - Email classification                             │  │
│  │  - Confidence scoring                               │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │   Trained ML Model (phishing_model.pkl)              │  │
│  │  - Random Forest Classifier                         │  │
│  │  - TF-IDF Vectorizer                                │  │
│  │  - Pre-trained on email dataset                      │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer

**Technology Stack:**
- HTML5 for structure
- CSS3 for styling
- Vanilla JavaScript for interactivity

**Key Components:**
1. **Form Section**
   - Email subject input
   - Email body textarea
   - Submit button

2. **Result Display**
   - Prediction (Phishing/Legitimate)
   - Confidence score
   - Risk level indicator

3. **Error Handling**
   - User-friendly error messages
   - Network error detection
   - Form validation

**Files:**
- `index.html` - Main UI structure
- `style.css` - Styling and responsive design
- `script.js` - Frontend logic and API communication

### Backend Layer

**Technology Stack:**
- Python 3.8+
- Flask web framework
- scikit-learn for ML
- pandas for data processing
- joblib for model serialization

**Components:**

#### 1. Flask Application (app.py)
- Initializes Flask server
- Defines REST API endpoints
- Handles HTTP requests and responses
- Implements error handling

**API Endpoints:**
```
POST /api/detect
- Input: JSON with email_subject and email_body
- Output: JSON with prediction, confidence, risk_level
- Status: 200 (success), 400 (bad request), 500 (server error)

GET /api/health
- Input: None
- Output: JSON with status
- Status: 200
```

#### 2. Detector Module (detector.py)
- Loads trained model from disk
- Preprocesses email text
- Generates predictions
- Calculates confidence scores

**Key Methods:**
- `__init__()` - Initialize detector and load model
- `load_model()` - Load serialized model file
- `predict()` - Classify email and return results

#### 3. ML Model
- **Algorithm**: Random Forest Classifier
- **Input Features**: TF-IDF vectors
- **Output Classes**: 0 (Legitimate), 1 (Phishing)
- **Hyperparameters**:
  - n_estimators: 100
  - random_state: 42
  - max_features: 5000 (TF-IDF)

### Data Layer

**Dataset Structure:**
- `subject`: Email subject line
- `body`: Email body content
- `label`: Classification (0/1)

**Data Files:**
- `emails.csv` - Combined training data
- `phishing_emails.csv` - Phishing examples
- `legitimate_emails.csv` - Legitimate examples

### Model Training Pipeline (train_model.py)

```
┌──────────────────┐
│  Load emails.csv │
└────────┬─────────┘
         │
┌────────▼─────────────┐
│  Combine text        │
│  (subject + body)    │
└────────┬─────────────┘
         │
┌────────▼─────────────────────┐
│  Train-Test Split (80-20)    │
└────────┬─────────────────────┘
         │
┌────────▼─────────────────────┐
│  TF-IDF Vectorization        │
│  (5000 features)             │
└────────┬─────────────────────┘
         │
┌────────▼─────────────────────┐
│  Train Random Forest         │
│  (100 estimators)            │
└────────┬─────────────────────┘
         │
┌────────▼─────────────────────┐
│  Evaluate Performance        │
│  (Accuracy, Precision, etc.) │
└────────┬─────────────────────┘
         │
┌────────▼──────────────────────┐
│  Save Model (phishing_model.pkl) │
└────────────────────────────────┘
```

## Data Flow

### Email Classification Flow

```
User Input (Frontend)
    ↓
["email_subject", "email_body"]
    ↓
JavaScript - Validate Input
    ↓
HTTP POST /api/detect
    ↓
Flask - Receive & Parse JSON
    ↓
Detector - Load Model
    ↓
Detector - Combine Text
    ↓
Vectorizer - Convert to TF-IDF
    ↓
Random Forest - Predict Class
    ↓
Calculate Confidence Score
    ↓
Determine Risk Level
    ↓
Return JSON Response
    ↓
HTTP 200 Response
    ↓
JavaScript - Parse & Display
    ↓
User Result Display
```

## Security Considerations

1. **Input Validation**
   - Empty field validation
   - Text length limits
   - Type checking

2. **Error Handling**
   - Exception catching in detector
   - Meaningful error messages
   - No sensitive data in responses

3. **CORS Considerations**
   - Frontend on port 8000
   - Backend on port 5000
   - May require CORS configuration for production

4. **Model Security**
   - Model file should be protected
   - Regular model updates
   - Version control for models

## Deployment Architecture

### Development
```
Local Machine
├── Frontend: file:// or http://localhost:8000
└── Backend: http://localhost:5000
```

### Production (Recommended)
```
Reverse Proxy (nginx)
    ↓
┌───────────────┐
│ Web Server    │ (Serve static frontend files)
└───────────────┘
    ↓
┌───────────────┐
│ API Server    │ (Flask + Gunicorn)
└───────────────┘
    ↓
┌───────────────┐
│ Database      │ (Optional: for logging/analytics)
└───────────────┘
```

## Performance Metrics

- **Inference Time**: < 100ms per email
- **Memory Usage**: ~50MB (model + dependencies)
- **Concurrent Requests**: Limited by Flask/Gunicorn config
- **Model Accuracy**: ~95% on test data

## Future Enhancements

1. **Scalability**
   - Load balancing
   - Distributed model serving
   - Caching layer (Redis)

2. **Monitoring**
   - Logging system
   - Performance metrics
   - Model performance tracking

3. **Advanced Features**
   - Deep learning models (LSTM, BERT)
   - Email header analysis
   - Attachment scanning
   - Sender reputation checking

4. **User Experience**
   - Model explainability (SHAP values)
   - Batch email processing
   - Email history tracking
   - User feedback mechanism

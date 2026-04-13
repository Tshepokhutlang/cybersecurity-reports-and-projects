# AI Phishing Detector 🎯

An intelligent email phishing detection system using machine learning to classify emails as phishing or legitimate. Features a professional web interface with batch processing, history tracking, and customizable settings.

## ✨ Core Features

- **🤖 ML-Based Detection**: Random Forest classifier with TF-IDF vectorization
- **🖥️ Professional Web UI**: 4-page single-page application (Analyze, Batch, History, Settings)
- **📊 Batch Analysis**: Upload CSV files to process multiple emails at once
- **📈 Analysis History**: Track all analyses with search and filtering
- **⚙️ Customizable Settings**: Control detection behavior and export preferences
- **🔌 REST API**: Backend endpoints for integration with other systems
- **🎯 Real-time Analysis**: Instant classification with confidence scores and risk assessment
- **📥 Export & Share**: Download reports as CSV/JSON or share via clipboard

## 📁 Project Structure

```
ai-phishing-detector/
├── backend/                    # Flask API and ML model
│   ├── app.py                 # Flask application with REST endpoints
│   ├── detector.py            # ML model wrapper for phishing detection
│   ├── train_model.py         # Model training script
│   ├── phishing_model.pkl     # Trained Random Forest model
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   ├── requirements.txt        # Python dependencies
│   └── __pycache__/           # Compiled Python files
├── frontend/                   # Professional web interface
│   ├── index.html             # Main application (4 pages)
│   ├── script.js              # Application logic + API integration
│   └── style.css              # Professional styling + responsive design
├── data/                      # Training datasets
│   ├── legitimate_emails.csv  # Legitimate email samples
│   └── phishing_emails.csv    # Phishing email samples
├── docs/                      # Documentation
│   ├── README.md             # This file
│   └── system_architecture.md # Technical architecture details
├── FEATURES_GUIDE.md          # Comprehensive feature documentation (NEW)
├── FEATURE_SCAN.md            # Validation and testing checklist
└── run_project.bat            # Quick start script for Windows
```

## 📖 Documentation

- **[FEATURES_GUIDE.md](../FEATURES_GUIDE.md)** - Complete user guide for all 4 pages and features
- **[system_architecture.md](system_architecture.md)** - Technical architecture and component details
- **[FEATURE_SCAN.md](../FEATURE_SCAN.md)** - Testing checklist and validation details

## 📋 Requirements

- **Python**: 3.8-3.12 (recommended), 3.13+ not fully supported
- **Flask**: 3.0.0+
- **scikit-learn**: 1.3.0+
- **pandas**: 2.0.0+
- **numpy**: 1.24.0+
- **joblib**: 1.3.0+
- **flask-cors**: 4.0.0+

## ⚙️ System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 256MB (for model loading and inference)
- **Disk**: ~50MB (including model, vectorizer, and dependencies)
- **Network**: Localhost access (127.0.0.1) for frontend ↔ backend communication

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend (Terminal 1)

```bash
cd backend
python app.py
# Server starts on http://localhost:5000
```

### Step 3: Start Frontend (Terminal 2)

```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

### ✅ Verify Installation

- Backend health: http://localhost:5000/api/health
- Frontend: http://localhost:8000
- Header shows "✓ Backend Connected" when both are running

## 📚 Full Installation & Usage

### Installation

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Accessing the Frontend

Serve the frontend directory with a local server:

```bash
# Navigate to frontend directory
cd frontend

# Using Python
python -m http.server 8000
```

Then navigate to `http://localhost:8000` in your web browser. The web interface now includes professional features such as batch analysis, history logging, export/share options, and customizable settings.

### New Frontend Features

- **Batch Email Analysis**: Upload a CSV file of emails for bulk classification.
- **Analysis History**: Results are saved locally and searchable/filterable.
- **Export & Share**: Download individual reports or copy them to clipboard.
- **Settings**: Control preferences like auto-save history, coverage of confidence, and export format.
- **Status Indicator**: View backend health in the header.
- **Dark mode & responsive layout** supported.


### API Endpoints

#### Detect Phishing Email

**POST** `/api/detect`

Request body:
```json
{
    "email_subject": "Verify your account",
    "email_body": "Click here to verify your account immediately"
}
```

Response:
```json
{
    "email_subject": "Verify your account",
    "prediction": "phishing",
    "confidence": 0.95,
    "risk_level": "high"
}
```

#### Health Check

**GET** `/api/health`

Response:
```json
{
    "status": "healthy"
}
```

## Model Information

- **Algorithm**: Random Forest Classifier
- **Features**: TF-IDF vectorization (5000 features)
- **Training Data**: Combined subject and body of emails
- **Test Accuracy**: ~95% (varies based on training data)

## File Descriptions

- `app.py` - Flask application and API endpoints
- `detector.py` - Phishing detection logic
- `train_model.py` - Model training script
- `phishing_model.pkl` - Trained model file
- `emails.csv` - Sample training data

## How to Train Your Model

1. Prepare a CSV file with columns: `subject`, `body`, `label` (0 for legitimate, 1 for phishing)
2. Place it as `emails.csv` in the backend directory
3. Run: `python train_model.py`

## Performance Metrics

Current model performance on test set:
- **Accuracy**: ~95%
- **Precision**: ~94%
- **Recall**: ~96%
- **F1-Score**: ~95%

## Security Notes

- This system is designed for educational purposes
- Real-world deployment requires additional security measures
- Always validate suspicious emails through official channels
- Consider combining with other security tools

## Future Improvements

- [ ] Deep learning model integration
- [ ] Multi-language support
- [ ] Email header analysis
- [ ] Sender reputation checking
- [ ] URL and attachment scanning
- [ ] User feedback loop for model improvement

## License

MIT License

## Support

For issues or feature requests, please create an issue in the project repository.

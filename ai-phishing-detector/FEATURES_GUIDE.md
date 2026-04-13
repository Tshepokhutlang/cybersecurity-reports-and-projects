# AI Phishing Detector - Complete Feature Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Train model (optional)
cd backend
python train_model.py
```

### Run the Application
```bash
# Terminal 1 - Start Backend (port 5000)
cd backend
python app.py

# Terminal 2 - Start Frontend (port 8000)
cd frontend
python -m http.server 8000
```

**Access the web app at**: http://localhost:8000

---

## 📊 Feature Overview

### 1️⃣ **ANALYZE EMAIL** (Single Email Detection)

#### Purpose
Analyze a single email to determine if it's phishing or legitimate.

#### How to Use
1. Go to **"Analyze Email"** tab
2. Enter the email subject line
3. Paste the email body
4. (Optional) Add sender email address
5. Select analysis mode:
   - **Standard**: Quick ML-based analysis
   - **Detailed**: With confidence metrics
   - **Comprehensive**: Full breakdown + recommendations
6. Click **"Analyze Email"**

#### What You'll See
- **Prediction**: PHISHING or LEGITIMATE
- **Confidence Level**: Visual meter (0-100%)
- **Risk Level**: HIGH, MEDIUM, or LOW
- **Threat Score**: Numerical risk assessment (0-100)
- **Analysis Time**: How long analysis took
- **Recommendations**: Actions to take
- **Detailed Breakdown**: Full analysis data (if enabled in settings)

#### Actions
- **Export Report**: Download analysis as JSON/CSV/PDF
- **Share Analysis**: Copy to clipboard for sharing
- **Clear Form**: Reset and start over

#### Example
```
Subject: Verify Your Account Now
Body: Click here immediately to confirm your PayPal login...

→ Result: PHISHING (92% confidence, HIGH risk)
→ Recommendations: Do not click. Report to security team.
```

---

### 2️⃣ **BATCH ANALYSIS** (Bulk Email Processing)

#### Purpose
Upload a CSV file with multiple emails for rapid processing and analysis.

#### How to Use
1. Go to **"Batch Analysis"** tab
2. Prepare a CSV file with columns: `subject,body`
3. Click **"Browse Files"** or drag-drop the CSV
4. Review file loaded message
5. Click **"Analyze Batch"**
6. Watch progress bar (real-time updates)
7. Download results when complete

#### CSV Format
```csv
subject,body
"Verify account","Click here to verify immediately"
"Team meeting","Meeting tomorrow at 2pm in room 101"
"Reset password","Use this link to reset your password"
```

#### Output
- **Total Emails**: Number processed
- **Phishing Detected**: Count of phishing emails
- **Legitimate**: Count of safe emails
- **Download Results**: CSV with all analyses

#### Features
- Real-time progress tracking
- Automatic statistics calculation
- Downloadable CSV report with predictions
- Optional auto-export on completion

#### Example Results CSV
```csv
subject,body,prediction,confidence
"Verify account","Click here...",phishing,0.92
"Team meeting","Meeting tomorrow...",legitimate,0.85
```

---

### 3️⃣ **ANALYSIS HISTORY** (View & Search Past Results)

#### Purpose
Access all previous email analyses with search and filtering capabilities.

#### How to Use
1. Go to **"Analysis History"** tab
2. **Search**: Type keywords (subject, sender, etc.)
3. **Filter**: Select "All Results", "Phishing Only", or "Legitimate Only"
4. **View Details**: Click any history entry to reload full results
5. **Clear History**: Delete all saved analyses

#### Features
- Auto-saves all analyses (if enabled in settings)
- Searchable by any field
- Filterable by prediction type
- Click-to-reload saves time re-analyzing
- Persistent storage (survives page refresh)

#### What's Stored
For each analysis:
- Email subject
- Prediction (phishing/legitimate)
- Confidence score
- Risk level
- Threat score
- Sender (if provided)
- Timestamp
- Analysis mode used

#### Example
```
History List:
- Verify your account → PHISHING (92%)
- Team meeting → LEGITIMATE (85%)
- Reset password → PHISHING (88%)
```

---

### 4️⃣ **SETTINGS** (Customize Experience)

#### Purpose
Control application behavior and preferences.

#### Settings Available

**Analysis Preferences:**
- ☑️ **Auto-save Analysis History**: Automatically save all results (default: ON)
- ☑️ **Show Confidence Percentages**: Display confidence on results (default: ON)
- ☑️ **Enable Detailed Analysis Breakdown**: Show full data breakdown (default: OFF)

**Notifications:**
- ☑️ **Notify on High-Risk Detections**: Alert for phishing (default: OFF)
- ☑️ **Enable Sound Alerts**: Beep on detection (default: OFF)

**Export Options:**
- Default Export Format:
  - PDF Report (formatted document)
  - CSV Data (spreadsheet compatible)
  - JSON Data (raw data export)

#### How to Change Settings
1. Go to **"Settings"** tab
2. Toggle checkboxes as desired
3. Select export format from dropdown
4. Click **"Save Settings"**
5. Settings persist across sessions

#### Settings Impact
- **Auto-save**: Enables/disables history auto-save
- **Show Confidence**: Toggles confidence display on results
- **Detailed Breakdown**: Shows/hides technical analysis data
- **Export Format**: Determines downloaded file type
- **Notifications**: Enables alerts for high-risk emails

---

## 🔌 Backend API Reference

### Endpoint: POST `/api/detect`

**Request:**
```json
{
  "email_subject": "string (required)",
  "email_body": "string (required)",
  "sender_email": "string (optional)",
  "analysis_mode": "string (optional)"
}
```

**Response:**
```json
{
  "email_subject": "string",
  "prediction": "phishing|legitimate",
  "confidence": 0.0-1.0,
  "risk_level": "high|medium|low",
  "threat_score": 0-100,
  "recommendations": ["string"],
  "sender_email": "string (if provided)",
  "analysis_time": "string (if provided)"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "Verify Account",
    "email_body": "Click to verify now"
  }'
```

**Example Response:**
```json
{
  "email_subject": "Verify Account",
  "prediction": "phishing",
  "confidence": 0.92,
  "risk_level": "high",
  "threat_score": 92.0,
  "recommendations": [
    "Do not click any links or download attachments.",
    "Report this email to your security team immediately."
  ]
}
```

### Endpoint: GET `/api/health`

**Purpose**: Check backend availability

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🛠️ Testing

### Manual Testing
Use the provided test script:

**Windows:**
```bash
test_api.bat
```

**Linux/Mac:**
```bash
bash test_api.sh
```

### Using curl (Windows PowerShell)
```powershell
# Test health
Invoke-WebRequest -Uri http://localhost:5000/api/health

# Test phishing detection
$body = @{
    email_subject = "Verify your account"
    email_body = "Click here to verify now"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/detect `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

---

## 🎯 Use Cases

### 1. Security Admin - Check Single Email
1. Receive suspicious email
2. Go to Analyze Email tab
3. Copy/paste email content
4. Get instant risk assessment
5. Export report if needed

### 2. IT Team - Audit Email Inbox
1. Export emails to CSV (subject, body columns)
2. Go to Batch Analysis
3. Upload CSV
4. Get statistics on phishing attempts
5. Download results for further investigation

### 3. User - Track Suspicious Emails
1. Enable auto-save history in settings
2. Analyze suspicious emails over time
3. Review history tab to see patterns
4. Filter to see all phishing attempts detected

### 4. Integration - API Access
1. POST requests to `/api/detect` endpoint
2. Parse JSON responses
3. Integrate into email security workflow
4. Automate phishing detection

---

## 📊 Data Persistence

### LocalStorage Managed by Browser
- **History**: Stored after each analysis
- **Settings**: Saved when you click "Save Settings"
- **Persistence**: Survives page refresh and browser restart
- **Limit**: ~5-10MB per browser (depends on email count)

### Clear Data
- History: Click "Clear History" in History tab
- Settings: Reset manually or delete browser cache

---

## 🔒 Security Notes

1. **Local Processing**: All analysis happens on local backend
2. **No Cloud**: Data doesn't leave your machine
3. **Private**: Emails stored only in browser localStorage
4. **CORS Enabled**: Safe cross-origin requests

---

## 🐛 Troubleshooting

### "Backend not responding"
- Check port 5000 is open: `netstat -ano | findstr :5000`
- Restart backend: `cd backend && python app.py`

### "Analysis History empty"
- Check "Auto-save history" is enabled in Settings
- Clear browser cache if disabled

### "File upload not working"
- Ensure CSV format: `subject,body`
- File must have at least 1 data row
- Check file size isn't too large (>10MB)

### "Confidence meter not showing"
- Enable "Show Confidence" in Settings
- Refresh page after changing settings

---

## 📈 Performance

- **Single Analysis**: ~100-500ms
- **Batch Analysis**: ~500ms per email
- **History Search**: <10ms
- **UI Response**: <50ms

---

## 🚀 Next Steps

1. **Configure Settings** for your workflow
2. **Test with Sample Emails** in Analyze tab
3. **Try Batch Processing** with multiple emails
4. **Review History** and Filter results
5. **Export Reports** as needed
6. **Share Access** to team members

---

## 📞 Support

For issues or feature requests, check:
- [GitHub Issues](link)
- [Documentation](docs/README.md)
- [System Architecture](docs/system_architecture.md)

---

**Version**: 2.0  
**Last Updated**: March 2026  
**Status**: ✅ Production Ready

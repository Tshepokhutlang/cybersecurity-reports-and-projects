@echo off
REM Test script for AI Phishing Detector (Windows)
REM Run this to validate all features

echo ==================================
echo AI Phishing Detector - Test Suite
echo ==================================
echo.

echo 1. Testing Backend Health...
curl -s http://localhost:5000/api/health
echo.
echo.

echo 2. Testing Phishing Detection...
curl -s -X POST http://localhost:5000/api/detect ^
  -H "Content-Type: application/json" ^
  -d "{\"email_subject\": \"Verify your account\", \"email_body\": \"Click here to verify your PayPal account immediately\"}"
echo.
echo.

echo 3. Testing Legitimate Email Detection...
curl -s -X POST http://localhost:5000/api/detect ^
  -H "Content-Type: application/json" ^
  -d "{\"email_subject\": \"Team meeting scheduled\", \"email_body\": \"Our team meeting is scheduled for tomorrow at 2pm in the conference room.\"}"
echo.
echo.

echo ==================================
echo Tests Complete!
echo ==================================
echo.
echo Access the web interface at: http://localhost:8000
echo.

pause

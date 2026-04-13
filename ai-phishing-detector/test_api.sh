#!/bin/bash
# Test script for AI Phishing Detector
# Run this to validate all features

echo "=================================="
echo "AI Phishing Detector - Test Suite"
echo "=================================="
echo ""

# Test 1: Backend health
echo "1. Testing Backend Health..."
curl -s http://localhost:5000/api/health | python -m json.tool
echo ""

# Test 2: Analyze a phishing email
echo "2. Testing Phishing Detection..."
curl -s -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "Verify your account",
    "email_body": "Click here to verify your PayPal account immediately"
  }' | python -m json.tool
echo ""

# Test 3: Analyze a legitimate email
echo "3. Testing Legitimate Email Detection..."
curl -s -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "Team meeting scheduled",
    "email_body": "Our team meeting is scheduled for tomorrow at 2pm in the conference room."
  }' | python -m json.tool
echo ""

echo "=================================="
echo "Tests Complete!"
echo "=================================="
echo ""
echo "Access the web interface at: http://localhost:8000"
echo ""

@echo off
REM AI Phishing Detector - Project Runner
REM This batch file starts both the backend and frontend servers

echo.
echo ====================================
echo   AI Phishing Detector Project
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "backend\" (
    echo Error: backend folder not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo Starting AI Phishing Detector...
echo.

REM Start backend in a new window
echo [1/2] Starting Backend Server on http://localhost:5000...
start "AI Phishing Detector - Backend" cmd /k "cd backend && python app.py"

REM Wait a few seconds for backend to start
timeout /t 3 /nobreak

REM Start frontend in default browser
echo [2/2] Opening Frontend in your browser...
start http://localhost:8000/index.html

REM Note about starting the frontend server
echo.
echo ====================================
echo   IMPORTANT: Starting Frontend Server
echo ====================================
echo.
echo You need to start a simple HTTP server for the frontend.
echo.
echo In a new terminal, run:
echo   cd frontend
echo   python -m http.server 8000
echo.
echo Or if you have Node.js installed, you can use:
echo   cd frontend
echo   npx http-server -p 8000
echo.
echo After starting the frontend server, open:
echo   http://localhost:8000/index.html
echo.
echo Backend API: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Press CTRL+C in either window to stop the servers
echo.

pause

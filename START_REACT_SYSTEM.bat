@echo off
title Speech Analyzer System
echo ========================================
echo   Speech Analyzer System Startup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not available
    echo Please install Node.js with npm and try again
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available
echo.

REM Install Python dependencies if needed
echo 📦 Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Could not install Python dependencies
) else (
    echo ✅ Python dependencies ready
)

REM Install Node.js dependencies if needed
echo 📦 Checking Node.js dependencies...
cd speech-analyzer-frontend
if not exist node_modules (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        cd ..
        pause
        exit /b 1
    )
)
cd ..
echo ✅ Node.js dependencies ready
echo.

echo 🚀 Starting services...
echo.

REM Start backend in a new window
echo 🔧 Starting Backend (Flask API)...
start "Backend - Flask API" cmd /k "python backend/app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo 🎨 Starting Frontend (React)...
start "Frontend - React" cmd /k "cd speech-analyzer-frontend && npm run dev"

REM Wait a moment for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   🎉 System Started Successfully!
echo ========================================
echo.
echo 🔗 Backend API: http://localhost:5000
echo 🌐 Frontend:    http://localhost:5173
echo.
echo 👤 Demo Login Credentials:
echo    Email:    demo@example.com
echo    Password: demo123
echo.
echo ⚠️  Keep both terminal windows open
echo    Close them to stop the services
echo.
echo 🌐 Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo Press any key to exit this window...
echo (The services will continue running in separate windows)
pause >nul
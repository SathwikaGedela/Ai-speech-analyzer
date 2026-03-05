@echo off
echo Starting AI Public Speaking Feedback System...
echo.
echo Opening web browser to http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server when done
echo.
start http://127.0.0.1:5000
python backend/app.py
pause
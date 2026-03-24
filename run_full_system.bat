@echo off
echo "Starting Backend..."
start cmd /k start_backend.bat
echo "Starting Frontend in 3s..."
timeout /t 3
start cmd /k start_frontend.bat
echo "Full system running!"
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
pause

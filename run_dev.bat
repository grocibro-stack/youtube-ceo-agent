@echo off
REM YouTube CEO Agent - Development Server Startup
REM This script starts the API server on localhost

cd /d "%~dp0"

echo.
echo ============================================
echo YouTube CEO Agent API - Local Development
echo ============================================
echo.
echo Server will be available at:
echo   http://127.0.0.1:8000
echo.
echo API Documentation (Swagger):
echo   http://127.0.0.1:8000/docs
echo.
echo Alternative Docs (ReDoc):
echo   http://127.0.0.1:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Activate venv and start server
call venv\Scripts\activate.bat
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause

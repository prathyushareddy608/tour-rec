@echo off
echo ============================================
echo Ticketless Entry System - Auto Setup
echo ============================================
echo.

REM Change to the project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed or not in PATH
    pause
    exit /b 1
)

echo Pip found:
pip --version
echo.

REM Install requirements
echo Installing Python requirements...
echo ============================================

REM Check if requirements.txt exists in current directory
if exist "requirements.txt" (
    echo Found requirements.txt in root directory
    pip install -r requirements.txt
) else if exist "Backend\requirements.txt" (
    echo Found requirements.txt in Backend directory
    pip install -r Backend\requirements.txt
) else (
    echo Installing common Django packages...
    pip install django djangorestframework django-cors-headers pillow qrcode razorpay
)

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install requirements
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo Requirements installed successfully!
echo.

REM Navigate to Backend directory
if exist "Backend" (
    echo Changing to Backend directory...
    cd Backend
) else (
    echo Backend directory not found, staying in current directory
)

echo Current directory: %CD%
echo.

REM Run Django migrations
echo Running Django migrations...
echo ============================================
python manage.py migrate

if errorlevel 1 (
    echo.
    echo WARNING: Migrations failed, but continuing...
    echo.
)

REM Collect static files (if needed)
echo Collecting static files...
python manage.py collectstatic --noinput

if errorlevel 1 (
    echo.
    echo WARNING: Static files collection failed, but continuing...
    echo.
)

echo.
echo ============================================
echo Starting Django Development Server...
echo ============================================
echo.
echo Server will start at: http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo Close this window to stop the application
echo.

REM Start the Django server
python manage.py runserver

REM If server stops, pause to show any error messages
echo.
echo Server stopped.
pause

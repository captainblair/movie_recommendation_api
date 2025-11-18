@echo off
REM Movie Recommendation API Setup Script for Windows

echo ==========================================
echo Movie Recommendation API - Setup Script
echo ==========================================

REM Check Python version
echo.
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
echo.
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your configuration.
) else (
    echo .env file already exists.
)

REM Create logs directory
echo.
echo Creating logs directory...
if not exist logs mkdir logs

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo.
echo Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput

REM Run tests
echo.
echo Running tests...
python manage.py test --verbosity 2

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Start the development server: python manage.py runserver
echo 2. Visit http://localhost:8000/api/docs/ for API documentation
echo 3. Visit http://localhost:8000/admin/ for Django admin
echo.
pause

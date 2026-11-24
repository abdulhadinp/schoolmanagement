@echo off
echo ================================================
echo  Library Management System - First Time Setup
echo ================================================

echo.
echo Step 1: Creating virtual environment...
python -m venv venv

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate

echo.
echo Step 3: Installing required packages...
pip install -r requirements.txt

echo.
echo Step 4: Checking for .env file...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo IMPORTANT: A ".env" file was created for you.
    echo Please open ".env" in a text editor NOW and enter your
    echo real MySQL username and password before continuing.
    echo.
    pause
) else (
    echo .env file already exists, skipping.
)

echo.
echo Step 5: Applying database migrations...
python manage.py migrate

echo.
echo ================================================
echo Setup complete!
echo Run "run.bat" to start the server, or create an
echo admin account first with:
echo     python manage.py createsuperuser
echo ================================================
pause

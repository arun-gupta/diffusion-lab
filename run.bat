@echo off
echo Starting Storyboard Generator...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and run the app
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting the application...
python app.py

pause 
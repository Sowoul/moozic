@echo off
setlocal

:: Check if requirements.txt exists
if not exist "requirements.txt" (
    echo Error: requirements.txt not found.
    exit /b 1
)

:: Install dependencies
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies.
    exit /b 1
)

:: Launch FlaskWebGui app
python main.py
if %errorlevel% neq 0 (
    echo Error launching the app.
    exit /b 1
)

endlocal

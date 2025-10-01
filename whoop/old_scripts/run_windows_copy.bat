@echo off
REM Windows batch file to run the Audio Recorder application
REM Double-click this file to start the application on Windows

echo Starting Audio Recorder with Webcam Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import sounddevice, numpy, tkinter, cv2" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        echo If OpenCV installation fails, try:
        echo pip install opencv-python-headless
        pause
        exit /b 1
    )
)

echo Dependencies OK. Starting application...
echo.

REM Run the application
python audio_recorder.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)

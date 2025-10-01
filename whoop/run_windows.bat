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




@REM @echo off
@REM REM Windows batch file to run Audio Recorder with Webcam + Flask server
@REM REM Optional: use --submit_previous_recordings to submit all existing recordings first

@REM echo Starting automated Audio Recorder system...
@REM echo.

@REM REM ------------------------
@REM REM Check if Python is installed
@REM REM ------------------------
@REM python --version >nul 2>&1
@REM if errorlevel 1 (
@REM     echo ERROR: Python is not installed or not in PATH
@REM     echo Please install Python from https://www.python.org/downloads/
@REM     echo Make sure to check "Add Python to PATH" during installation
@REM     pause
@REM     exit /b 1
@REM )

@REM REM ------------------------
@REM REM Check required Python packages
@REM REM ------------------------
@REM echo Checking dependencies...
@REM python -c "import sounddevice, numpy, tkinter, cv2, flask, requests" >nul 2>&1
@REM if errorlevel 1 (
@REM     echo Installing required Python packages...
@REM     python -m pip install --upgrade pip
@REM     python -m pip install -r requirements.txt
@REM     if errorlevel 1 (
@REM         echo ERROR: Failed to install dependencies
@REM         echo Please run: pip install -r requirements.txt
@REM         pause
@REM         exit /b 1
@REM     )
@REM )

@REM REM ------------------------
@REM REM Start Flask server in background
@REM REM ------------------------
@REM echo Starting Flask server...
@REM start "" /B python server.py
@REM REM Wait 2 seconds for server to initialize
@REM timeout /t 2 >nul

@REM REM ------------------------
@REM REM Submit all existing recordings if flag is provided
@REM REM ------------------------
@REM if "%1"=="--submit_previous_recordings" (
@REM     echo Submitting all existing recordings from recordings folder...
@REM     python submit_all_recordings.py
@REM )

@REM REM ------------------------
@REM REM Launch Audio Recorder GUI
@REM REM ------------------------
@REM echo Launching Audio Recorder GUI...
@REM python audio_recorder.py

@REM REM ------------------------
@REM REM After GUI exits, terminate Flask server
@REM REM ------------------------
@REM echo GUI closed. Attempting to terminate Flask server...
@REM REM Taskkill all python.exe running server.py (be careful if other Python processes are running)
@REM for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /v ^| findstr "server.py"') do taskkill /PID %%i /F

@REM echo Done.
@REM pause

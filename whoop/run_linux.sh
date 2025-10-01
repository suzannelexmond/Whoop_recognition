#!/bin/bash
# Linux shell script to run Audio Recorder with Webcam + Flask server
# Optional: submit all existing recordings first with --submit-all

echo "Starting automated Audio Recorder system..."
echo

# ------------------------
# Check Python3
# ------------------------
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not installed."
    exit 1
fi

# ------------------------
# System dependencies for sounddevice
# ------------------------
sudo apt update -y
sudo apt install -y libportaudio2 libportaudiocpp0 portaudio19-dev python3-pip

# ------------------------
# Install required Python packages
# ------------------------
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# ------------------------
# Start Flask server in background
# ------------------------
echo "Starting Flask server..."
python3 server.py &
FLASK_PID=$!

# Wait a second for the server to start
sleep 2

# ------------------------
# Submit all recordings if flag is provided
# ------------------------
if [ "$1" == "--submit_previous_recordings" ]; then
    echo "Submitting all existing recordings from /whoop/recordings ..."
    python3 submit_all_recordings.py
fi

# ------------------------
# Launch Audio Recorder GUI
# ------------------------
echo "Launching Audio Recorder GUI..."
python3 audio_recorder.py

# ------------------------
# After GUI exits, terminate Flask server
# ------------------------
echo "GUI closed. Shutting down Flask server..."
kill $FLASK_PID


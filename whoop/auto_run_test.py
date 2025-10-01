# import subprocess
# import time
# import webbrowser

# # 1️⃣ Start Flask server
# server_script = "server.py"
# server_proc = subprocess.Popen(["python3", server_script])
# time.sleep(2)  # wait for server to start

# # 2️⃣ Launch Audio Recorder GUI (non-blocking)
# recorder_script = "audio_recorder.py"
# recorder_proc = subprocess.Popen(["python3", recorder_script])

# # 3️⃣ Open leaderboard in browser
# webbrowser.open("http://127.0.0.1:5500/leaderboard.html")

# # 4️⃣ Keep everything running
# try:
#     recorder_proc.wait()
# except KeyboardInterrupt:
#     print("Shutting down...")
#     recorder_proc.terminate()
#     server_proc.terminate()


import os
import time
import subprocess
import requests
import webbrowser
from pathlib import Path

# # 1️⃣ Launch Audio Recorder GUI
# recorder_script = "audio_recorder.py"
# subprocess.run(["python3", recorder_script])  # waits until the GUI is closed

# # 2️⃣ Get the latest .wav file from recordings folder
# recordings_dir = Path("recordings")
# wav_files = sorted(recordings_dir.glob("*.wav"), key=os.path.getmtime)
# if not wav_files:
#     raise FileNotFoundError("No .wav files found in recordings folder!")

# # latest_wav = wav_files[-1]  # latest recording
latest_wav = 'recordings/Brecht_20250919_174917.wav'
print(f"Latest recording detected: {latest_wav}")

# 3️⃣ Run whoop.py on this file and get the dictionary
score_script = "whoop_gamescore.py"
# Use subprocess to capture stdout as JSON-like string
result = subprocess.run(["python3", score_script, str(latest_wav)],
                        capture_output=True, text=True)
print(f'score calculation succeeded: {result}')
# Attempt to evaluate output as dictionary
try:
    # whoop.py prints "Mean match of mimic and real chirp: ..." and returns result
    # To properly capture dictionary, modify whoop.py to `print(result)` at the end
    score_dict = eval(result.stdout.strip())
except Exception as e:
    raise RuntimeError(f"Failed to get result from whoop.py: {e}")

print("Score dict:", score_dict)

# 4️⃣ Start Flask server
server_script = "server.py"
server_proc = subprocess.Popen(["python3", server_script])
time.sleep(2)  # wait for server to start

# 5️⃣ POST the score to the server
try:
    response = requests.post("http://127.0.0.1:5000/submit-score", json=score_dict)
    print("Score submitted:", score_dict)
except Exception as e:
    print("Failed to submit score:", e)

# 6️⃣ Open leaderboard
webbrowser.open("http://127.0.0.1:5500/leaderboard.html")

# Optional: Keep server running until user closes script
try:
    server_proc.wait()
except KeyboardInterrupt:
    server_proc.terminate()

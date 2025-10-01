#!/usr/bin/env python3
import os
import subprocess
import requests
from pathlib import Path

# URL of your Flask server
SERVER_URL = "http://127.0.0.1:5000/submit-score"

# Path to the recordings folder
RECORDINGS_DIR = Path("recordings")

def submit_wav(wav_path):
    """Run whoop.py on a WAV file and POST the result to the server"""
    try:
        # Run whoop.py and capture output
        result = subprocess.run(
            ["python3", "whoop_gamescore.py", str(wav_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Whoop.py failed for {wav_path}: {result.stderr.strip()}")
            return

        # Parse the output as a dictionary
        try:
            score_dict = eval(result.stdout.strip())
        except Exception as e:
            print(f"❌ Failed to parse whoop.py output for {wav_path}: {e}")
            return

        # POST to server
        response = requests.post(SERVER_URL, json=score_dict)
        if response.status_code == 200:
            print(f"✅ Submitted {wav_path}: {score_dict}")
        else:
            print(f"❌ Failed to submit {wav_path}: {response.text}")

    except Exception as e:
        print(f"❌ Error processing {wav_path}: {e}")


def main():
    # Check recordings folder
    if not RECORDINGS_DIR.exists():
        print(f"❌ Recordings folder not found: {RECORDINGS_DIR}")
        return

    wav_files = sorted(RECORDINGS_DIR.glob("*.wav"))
    if not wav_files:
        print(f"❌ No .wav files found in {RECORDINGS_DIR}")
        return

    print(f"Submitting {len(wav_files)} recordings to server...")

    for wav in wav_files:
        submit_wav(wav)

    print("✅ Done submitting all recordings.")


if __name__ == "__main__":
    main()

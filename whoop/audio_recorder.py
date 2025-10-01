#!/usr/bin/env python3
"""
Simple Tkinter Audio Recording Application

This application provides a GUI with:
- A text field to enter a name
- A button to start the recording process
- A countdown timer before recording starts
- 5-second audio recording capability
- Saves recordings with the provided name

Cross-platform compatible: Windows, macOS, Linux
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import wave
import sounddevice as sd
import numpy as np
import os
import platform
import re
from datetime import datetime
import cv2
import subprocess
import requests


class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Recording parameters
        self.sample_rate = 44100  # Hz
        self.duration = 5  # seconds
        self.countdown_time = 3  # seconds
        self.recording_data = None
        self.is_recording = False
        
        # Webcam parameters
        self.webcam = None
        self.webcam_available = False
        self.video_writer = None
        
        # Check audio device availability on startup
        self.check_audio_devices()
        
        # Check webcam availability on startup
        self.check_webcam_devices()
        
        self.setup_ui()
        
    def check_audio_devices(self):
        """Check if audio input devices are available"""
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            
            if not input_devices:
                # Show warning but don't prevent startup
                system_name = platform.system()
                if system_name == "Windows":
                    warning_msg = ("No audio input devices detected.\n\n"
                                 "On Windows, make sure:\n"
                                 "• Your microphone is connected and enabled\n"
                                 "• Windows has microphone permissions for Python\n" 
                                 "• Check Windows Sound settings")
                else:
                    warning_msg = ("No audio input devices detected.\n"
                                 "Please check your microphone connection and system audio settings.")
                
                messagebox.showwarning("Audio Device Warning", warning_msg)
                
        except Exception as e:
            messagebox.showwarning("Audio System Warning", 
                                 f"Could not check audio devices: {str(e)}\n"
                                 "Recording may not work properly.")
        
    def check_webcam_devices(self):
        """Check if webcam devices are available"""
        try:
            # Try to access the default camera (index 0)
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                self.webcam_available = True
                cap.release()
            else:
                self.webcam_available = False
                
                # Provide Windows-specific guidance
                if platform.system() == "Windows":
                    warning_msg = ("No webcam detected or webcam is in use by another application.\n\n"
                                 "On Windows, make sure:\n"
                                 "• Your webcam is connected and recognized by Windows\n"
                                 "• Windows has camera permissions for Python applications\n"
                                 "• Go to Settings → Privacy & Security → Camera → Allow desktop apps\n"
                                 "• Close other apps that might be using the camera (Zoom, Skype, Teams)\n"
                                 "• Test your camera with the Windows Camera app first\n\n"
                                 "Video recording will be disabled - audio recording will continue to work.")
                else:
                    warning_msg = ("No webcam detected or webcam is in use by another application.\n"
                                 "Video recording will be disabled.")
                
                messagebox.showwarning("Webcam Warning", warning_msg)
        except Exception as e:
            self.webcam_available = False
            
            # Enhanced error message for Windows
            if platform.system() == "Windows":
                error_msg = (f"Could not check webcam devices: {str(e)}\n\n"
                           "This might be due to:\n"
                           "• Missing or incompatible camera drivers\n"
                           "• Windows camera privacy settings\n"
                           "• OpenCV installation issues\n\n"
                           "Try running: pip install --upgrade opencv-python\n"
                           "Video recording will be disabled.")
            else:
                error_msg = (f"Could not check webcam devices: {str(e)}\n"
                           "Video recording will be disabled.")
            
            messagebox.showwarning("Webcam System Warning", error_msg)
        
    def sanitize_filename(self, filename):
        """Sanitize filename for cross-platform compatibility, especially Windows"""
        # Remove or replace invalid characters for Windows filenames
        # Invalid characters: < > : " | ? * \ /
        invalid_chars = r'<>:"|?*\/'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
            
        # Remove leading/trailing dots and spaces (Windows issue)
        filename = filename.strip('. ')
        
        # Ensure filename is not empty
        if not filename:
            filename = "recording"
            
        # Windows reserved names
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                         'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        if filename.upper() in reserved_names:
            filename = f"user_{filename}"
            
        return filename
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio Recorder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name input
        name_label = ttk.Label(main_frame, text="Your Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, 
                                   width=30, font=("Arial", 11))
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status display
        self.status_var = tk.StringVar(value="Enter your name and click 'Start Recording'")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Arial", 10))
        status_label.grid(row=2, column=0, columnspan=2, pady=(20, 10))
        
        # Countdown display
        self.countdown_var = tk.StringVar(value="")
        self.countdown_label = ttk.Label(main_frame, textvariable=self.countdown_var, 
                                        font=("Arial", 24, "bold"), 
                                        foreground="red")
        self.countdown_label.grid(row=3, column=0, columnspan=2, pady=(10, 20))
        
        # Record button
        self.record_button = ttk.Button(main_frame, text="Start Recording", 
                                       command=self.start_recording_process)
        self.record_button.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # Progress bar for recording
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Instructions
        instructions = ("Instructions:\n"
                       "1. Enter your name in the text field\n"
                       "2. Click 'Start Recording'\n"
                       "3. Wait for the countdown to finish\n"
                       "4. Recording will start automatically for 5 seconds\n"
                       "5. Audio and video files will be saved with your name")
        
        # Add webcam status to instructions
        if self.webcam_available:
            instructions += "\n\n✅ Webcam detected - Video recording enabled"
        else:
            instructions += "\n\n⚠️ No webcam detected - Audio only"
        
        instructions_label = ttk.Label(main_frame, text=instructions, 
                                      font=("Arial", 9), 
                                      justify=tk.LEFT)
        instructions_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
    def start_recording_process(self):
        """Start the recording process with countdown"""
        name = self.name_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter your name first!")
            return
            
        if self.is_recording:
            messagebox.showinfo("Info", "Recording is already in progress!")
            return
        
        # Disable the button and start the process
        self.record_button.config(state='disabled')
        
        # Pre-initialize webcam if available to avoid delay after countdown
        if self.webcam_available:
            try:
                self.webcam = cv2.VideoCapture(0)
                if not self.webcam.isOpened():
                    print("Warning: Could not open webcam, falling back to audio-only")
                    self.webcam_available = False
                    if self.webcam:
                        self.webcam.release()
                        self.webcam = None
                else:
                    # Set webcam properties for better Windows compatibility
                    if platform.system() == "Windows":
                        # Set buffer size to reduce latency on Windows
                        self.webcam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                        # Set frame format for better compatibility
                        self.webcam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            except Exception as e:
                print(f"Warning: Webcam initialization failed: {e}")
                self.webcam_available = False
                if self.webcam:
                    self.webcam.release()
                    self.webcam = None
        
        # Start countdown and recording in a separate thread
        thread = threading.Thread(target=self.recording_thread)
        thread.daemon = True
        thread.start()
        
    def recording_thread(self):
        """Handle countdown and recording in a separate thread"""
        try:
            # Countdown phase
            self.status_var.set("Get ready! Recording will start in...")
            
            for i in range(self.countdown_time, 0, -1):
                self.countdown_var.set(str(i))
                time.sleep(1)
                
            self.countdown_var.set("")
            
            # Recording phase
            status_text = "🔴 RECORDING... Speak now!"
            if self.webcam_available:
                status_text += " (Audio + Video)"
            self.status_var.set(status_text)
            self.is_recording = True
            
            # Start progress bar
            self.progress['maximum'] = self.duration * 10  # Update every 0.1 seconds
            self.progress['value'] = 0
            
            # New approach: Record video with audio synchronously if webcam available
            if self.webcam_available:
                self.record_video_with_audio()
            else:
                # Record audio only
                self.record_audio_only()
            
            # Save the recordings
            self.save_recording()
            
        except Exception as e:
            messagebox.showerror("Error", f"Recording failed: {str(e)}")
        finally:
            # Reset UI
            self.is_recording = False
            self.status_var.set("Enter your name and click 'Start Recording'")
            self.countdown_var.set("")
            self.progress['value'] = 0
            self.record_button.config(state='normal')
            
            # Cleanup webcam if it was initialized for this recording
            if hasattr(self, 'webcam') and self.webcam:
                self.webcam.release()
                self.webcam = None
            
    def record_video_with_audio(self):
        """Record video and audio synchronously to avoid timing issues"""
        try:
            # Webcam should already be initialized in start_recording_process
            if not self.webcam or not self.webcam.isOpened():
                print("Warning: Webcam not available for recording")
                # Fall back to audio only
                self.record_audio_only()
                return
            
            # Get webcam properties
            fps = 30  # Frame rate
            width = int(self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Ensure we have valid dimensions
            if width <= 0 or height <= 0:
                width, height = 640, 480  # Default resolution
                print(f"Warning: Invalid webcam resolution, using default {width}x{height}")
            
            # Create video filename
            name = self.name_var.get().strip()
            safe_name = self.sanitize_filename(name) if name else "anonymous"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"{safe_name}_{timestamp}.mp4"
            
            # Ensure recordings directory exists
            recordings_dir = os.path.join(os.getcwd(), "recordings")
            if not os.path.exists(recordings_dir):
                os.makedirs(recordings_dir, exist_ok=True)
            
            video_filepath = os.path.join(recordings_dir, video_filename)
            
            # Initialize video writer (MP4 codec, no audio)
            # Use Windows-compatible codec selection
            if platform.system() == "Windows":
                # Try different codecs for better Windows compatibility
                codecs_to_try = ['mp4v', 'XVID', 'MJPG', 'WMV2']
                self.video_writer = None
                
                for codec_name in codecs_to_try:
                    try:
                        fourcc = cv2.VideoWriter_fourcc(*codec_name)
                        self.video_writer = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))
                        if self.video_writer.isOpened():
                            break
                        else:
                            self.video_writer.release()
                    except:
                        continue
                
                if not self.video_writer or not self.video_writer.isOpened():
                    print("Warning: Could not initialize video writer with any codec")
                    # Fall back to audio only
                    self.record_audio_only()
                    return
            else:
                # Use default codec for other platforms
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                self.video_writer = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))
            
            # Verify video writer is working
            if not self.video_writer.isOpened():
                print("Warning: Video writer could not be initialized")
                # Fall back to audio only
                self.record_audio_only()
                return
            
            # Start audio recording in the background
            self.recording_data = sd.rec(int(self.duration * self.sample_rate), 
                                       samplerate=self.sample_rate, 
                                       channels=1, dtype=np.float32)
            
            # Record video for the duration - synchronized with audio
            start_time = time.time()
            frame_count = 0
            target_frames = fps * self.duration
            
            while time.time() - start_time < self.duration and frame_count < target_frames:
                ret, frame = self.webcam.read()
                if ret:
                    self.video_writer.write(frame)
                    frame_count += 1
                else:
                    # Handle frame read failures
                    print("Warning: Failed to read frame from webcam")
                    break
                
                # Update progress bar
                progress_value = int((time.time() - start_time) * 10)
                if progress_value <= self.duration * 10:
                    self.progress['value'] = progress_value
                
                time.sleep(1.0 / fps)  # Maintain frame rate
            
            # Wait for audio recording to complete
            sd.wait()
            
            print(f"Recorded {frame_count} video frames")
            
        except Exception as e:
            error_msg = f"Error during synchronized recording: {e}"
            print(error_msg)
            # On Windows, provide additional troubleshooting info
            if platform.system() == "Windows":
                print("Windows troubleshooting:")
                print("- Check camera permissions in Windows Settings")
                print("- Close other apps using the camera")
                print("- Try running as administrator")
            # Fall back to audio only
            self.record_audio_only()
        finally:
            # Cleanup webcam resources
            if hasattr(self, 'video_writer') and self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            if hasattr(self, 'webcam') and self.webcam:
                self.webcam.release()
                self.webcam = None
    
    def record_audio_only(self):
        """Record audio only when no webcam is available"""
        try:
            # Record audio
            self.recording_data = sd.rec(int(self.duration * self.sample_rate), 
                                       samplerate=self.sample_rate, 
                                       channels=1, dtype=np.float32)
            
            # Update progress bar during recording
            for i in range(self.duration * 10):
                time.sleep(0.1)
                self.progress['value'] = i + 1
                
            sd.wait()  # Wait until recording is finished
            
        except Exception as e:
            print(f"Error during audio recording: {e}")
            raise
    
    def save_recording(self):
        """Save the recorded audio to a WAV file and automatically score it."""
        try:
            name = self.name_var.get().strip()
            safe_name = self.sanitize_filename(name) if name else "anonymous"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.wav"

            # Ensure recordings directory exists
            recordings_dir = os.path.join(os.getcwd(), "recordings")
            os.makedirs(recordings_dir, exist_ok=True)

            filepath = os.path.join(recordings_dir, filename)

            # Convert float32 to int16 and save WAV
            audio_data = (self.recording_data * 32767).astype(np.int16)
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes per sample
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())

            self.status_var.set(f"✅ Recording saved as: {filename}")

            # Prepare success message
            success_msg = f"Recording saved successfully!\nAudio file: {filename}\nLocation: {recordings_dir}"

            # Include video file if available
            if self.webcam_available:
                video_filename = f"{safe_name}_{timestamp}.mp4"
                video_filepath = os.path.join(recordings_dir, video_filename)
                if os.path.exists(video_filepath):
                    success_msg += f"\nVideo file: {video_filename}"
                else:
                    success_msg += "\nNote: Video recording may have failed"

            messagebox.showinfo("Success", success_msg)

            # ---- AUTOMATIC SCORING ----
            try:
                # Run whoop.py on the saved WAV
                result = subprocess.run(
                    ["python3", "whoop_gamescore.py", filepath],
                    capture_output=True, text=True
                )

                if result.returncode == 0:
                    # whoop.py must print a dictionary like {"name": "Alice", "score": 0.87}
                    score_dict = eval(result.stdout.strip())
                    print("Whoop.py output:", score_dict)

                    # Submit score to Flask server
                    try:
                        requests.post("http://127.0.0.1:5000/submit-score", json=score_dict)
                        print("Score submitted successfully!")
                    except Exception as e:
                        print("Failed to submit score:", e)
                else:
                    print("Whoop.py error:", result.stderr.strip())

            except Exception as e:
                print("Error running whoop.py:", e)

        except Exception as e:
            error_msg = f"Failed to save recording: {str(e)}"
            self.status_var.set("❌ Save failed - check console")
            messagebox.showerror("Error", error_msg)



def main():
    """Main function to run the application"""
    try:
        # Handle Windows-specific DPI awareness for better GUI scaling
        if platform.system() == "Windows":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass  # Ignore if not available
                
        root = tk.Tk()
        
        # Set window icon if available (cross-platform)
        try:
            # On Windows, this will work if there's an .ico file
            # On other platforms, it will be ignored or use a different format
            root.iconbitmap(default='audio_icon.ico')
        except:
            pass  # Ignore if icon file not found
            
        app = AudioRecorderApp(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication closed by user")
            
    except Exception as e:
        # Handle any startup errors gracefully
        error_msg = f"Failed to start application: {str(e)}"
        print(error_msg)
        try:
            import tkinter.messagebox as mb
            mb.showerror("Startup Error", error_msg)
        except:
            pass


if __name__ == "__main__":
    main()
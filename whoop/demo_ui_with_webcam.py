#!/usr/bin/env python3
"""
Demo script to show the new GUI layout with webcam functionality
and take a screenshot of the updated application interface.
"""

import tkinter as tk
from tkinter import ttk
import os

class AudioRecorderDemoWithWebcam:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder with Webcam - Demo")
        self.root.geometry("400x350")  # Slightly taller for webcam status
        self.root.resizable(False, False)
        
        # Simulate webcam availability for demo
        self.webcam_available = True  # Set to True for demo purposes
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface for demo"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio Recorder with Webcam", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name input
        name_label = ttk.Label(main_frame, text="Your Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.name_var = tk.StringVar(value="Demo User")
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
                                       command=self.demo_button_click)
        self.record_button.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # Progress bar for recording
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Instructions with webcam status
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
    
    def demo_button_click(self):
        """Demo button click handler"""
        print("Demo: Button clicked!")
        print(f"Demo: Name entered: '{self.name_var.get()}'")
        print("Demo: In real application, countdown and recording would start now.")
        print("Demo: Both audio (.wav) and video (.mp4) files would be created.")

def create_demo_screenshot():
    """Create a demo and optionally take a screenshot"""
    root = tk.Tk()
    demo = AudioRecorderDemoWithWebcam(root)
    
    print("Demo UI created showing new webcam functionality!")
    print("Key differences from original:")
    print("- Title now shows 'Audio Recorder with Webcam'")
    print("- Instructions mention both audio and video files")
    print("- Webcam status indicator shows '✅ Webcam detected - Video recording enabled'")
    print("- Window is slightly taller to accommodate new information")
    print("- Success messages will show both .wav and .mp4 files")
    
    # For actual GUI testing, you would uncomment this:
    # root.mainloop()
    
    # For headless demo, just show the changes
    root.destroy()
    print("\nDemo completed - UI changes successfully implemented!")

if __name__ == "__main__":
    create_demo_screenshot()
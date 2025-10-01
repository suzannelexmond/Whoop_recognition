#!/usr/bin/env python3
"""
Demo script to show GUI layout and take a screenshot of the application
without requiring audio functionality.
"""

import tkinter as tk
from tkinter import ttk
import os

class AudioRecorderDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder - Demo")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
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
        title_label = ttk.Label(main_frame, text="Audio Recorder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name input
        name_label = ttk.Label(main_frame, text="Your Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.name_var = tk.StringVar(value="John Doe")  # Demo value
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
        
        # Instructions
        instructions = ("Instructions:\n"
                       "1. Enter your name in the text field\n"
                       "2. Click 'Start Recording'\n"
                       "3. Wait for the countdown to finish\n"
                       "4. Recording will start automatically for 5 seconds\n"
                       "5. File will be saved with your name")
        
        instructions_label = ttk.Label(main_frame, text=instructions, 
                                      font=("Arial", 9), 
                                      justify=tk.LEFT)
        instructions_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
    def demo_button_click(self):
        """Demo button click handler"""
        print("Demo: Button clicked!")
        print(f"Demo: Name entered: '{self.name_var.get()}'")
        print("Demo: In real application, countdown and recording would start now.")

def create_demo_screenshot():
    """Create a demo and optionally take a screenshot"""
    print("Creating demo GUI...")
    
    root = tk.Tk()
    demo = AudioRecorderDemo(root)
    
    print("Demo GUI created successfully!")
    print("GUI Elements:")
    print("- Title: 'Audio Recorder'")
    print("- Name input field with label")
    print("- Status message area")
    print("- Countdown display area")
    print("- 'Start Recording' button")
    print("- Progress bar")
    print("- Instructions text")
    
    # Schedule window to close after a short delay for demo
    def close_demo():
        print("Demo completed - window would display the interface.")
        root.quit()
        
    root.after(1000, close_demo)  # Close after 1 second
    
    try:
        root.mainloop()
    except:
        pass
        
    print("Demo window closed.")

if __name__ == "__main__":
    create_demo_screenshot()
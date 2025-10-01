#!/usr/bin/env python3
"""
Example usage demonstration of the audio recorder application.

This script shows how the application components work together
and demonstrates the expected flow.
"""

import os
import sys

def show_usage_example():
    """Show example usage of the audio recorder application"""
    print("="*60)
    print("AUDIO RECORDER APPLICATION - USAGE EXAMPLE")
    print("="*60)
    
    print("\n1. INSTALLATION:")
    print("   pip3 install -r requirements.txt")
    
    print("\n2. RUNNING THE APPLICATION:")
    print("   python3 audio_recorder.py")
    
    print("\n3. APPLICATION FLOW:")
    print("   a) GUI window opens with the following elements:")
    print("      - Title: 'Audio Recorder'")
    print("      - Name input field labeled 'Your Name:'")
    print("      - Status message area")
    print("      - Countdown display (red, large font)")
    print("      - 'Start Recording' button")
    print("      - Progress bar for recording feedback")
    print("      - Instructions panel")
    
    print("\n   b) User enters their name (e.g., 'John Doe')")
    
    print("\n   c) User clicks 'Start Recording' button")
    print("      - Button becomes disabled")
    print("      - Status shows: 'Get ready! Recording will start in...'")
    
    print("\n   d) 3-second countdown begins:")
    print("      - Large red numbers: '3', '2', '1'")
    print("      - Each number displays for 1 second")
    
    print("\n   e) Recording phase (5 seconds):")
    print("      - Status shows: '🔴 RECORDING... Speak now!'")
    print("      - Progress bar fills up over 5 seconds")
    print("      - Audio is captured from default microphone")
    
    print("\n   f) File saving:")
    print("      - Creates 'recordings/' directory if needed")
    print("      - Saves as: 'John_Doe_20240316_143052.wav'")
    print("      - Status shows: '✅ Recording saved as: [filename]'")
    print("      - Success message box appears")
    
    print("\n   g) UI resets:")
    print("      - Button becomes enabled again")
    print("      - Progress bar resets")
    print("      - Ready for next recording")
    
    print("\n4. FILE OUTPUT:")
    print("   - WAV format, 44.1kHz sample rate, mono")
    print("   - Filename includes name and timestamp")
    print("   - Stored in 'recordings/' directory")
    
    print("\n5. ERROR HANDLING:")
    print("   - Name validation (must not be empty)")
    print("   - Audio device availability checks")
    print("   - File saving error handling")
    print("   - User-friendly error messages")
    
    print("\n6. FEATURES:")
    print("   ✅ Simple, intuitive GUI")
    print("   ✅ Clear countdown with visual feedback")
    print("   ✅ Progress indication during recording")
    print("   ✅ Automatic file naming with timestamps")
    print("   ✅ Error handling and user feedback")
    print("   ✅ Cross-platform compatibility")
    
    print("\n" + "="*60)
    print("Ready to use! Run: python3 audio_recorder.py")
    print("="*60)

if __name__ == "__main__":
    show_usage_example()
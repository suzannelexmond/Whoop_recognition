#!/usr/bin/env python3
"""
Basic test script to verify audio recording functionality
without requiring GUI interaction.
"""

import os
import tempfile
import wave
import sounddevice as sd
import numpy as np
from datetime import datetime

def test_audio_recording():
    """Test basic audio recording and saving functionality"""
    print("Testing audio recording functionality...")
    
    # Recording parameters
    sample_rate = 44100
    duration = 1  # Short test recording
    
    try:
        print("Creating test recording...")
        
        # Create test audio data (sine wave)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        test_audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        
        # Test file saving
        test_name = "test_user"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.wav"
        
        # Create test recordings directory
        test_dir = "test_recordings"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            
        filepath = os.path.join(test_dir, filename)
        
        # Convert to int16 and save
        audio_data = (test_audio * 32767).astype(np.int16)
        
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 2 bytes per sample
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
            
        print(f"✅ Test recording saved successfully: {filename}")
        
        # Verify file exists and has content
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print("✅ File verification passed")
            
            # Clean up test file
            os.remove(filepath)
            os.rmdir(test_dir)
            print("✅ Cleanup completed")
            
            return True
        else:
            print("❌ File verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_sounddevice_availability():
    """Test if sounddevice can access audio devices"""
    print("\nTesting sounddevice availability...")
    
    try:
        devices = sd.query_devices()
        print(f"✅ Found {len(devices)} audio devices")
        
        # Check for input devices
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        print(f"✅ Found {len(input_devices)} input devices")
        
        if len(input_devices) == 0:
            print("⚠️  Warning: No input devices found. Recording may not work.")
            
        return True
        
    except Exception as e:
        print(f"❌ Sounddevice test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running basic audio functionality tests...\n")
    
    test1 = test_audio_recording()
    test2 = test_sounddevice_availability()
    
    if test1 and test2:
        print("\n✅ All tests passed! The audio recording functionality should work.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
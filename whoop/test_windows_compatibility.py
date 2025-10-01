#!/usr/bin/env python3
"""
Windows compatibility test script for the audio recorder application.
Tests various Windows-specific scenarios and compatibility issues.
"""

import os
import platform
import sys
from datetime import datetime

def test_windows_filename_sanitization():
    """Test filename sanitization for Windows compatibility"""
    print("Testing Windows filename sanitization...")
    
    # Import the AudioRecorderApp class
    sys.path.insert(0, os.path.dirname(__file__))
    from audio_recorder import AudioRecorderApp
    
    # Create a dummy app instance for testing
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the window for testing
    app = AudioRecorderApp(root)
    
    # Test cases with problematic Windows filenames
    test_cases = [
        ("John<Doe", "John_Doe"),
        ("Test>File", "Test_File"),
        ("My:Audio", "My_Audio"),
        ('File"Name', "File_Name"),
        ("Audio|Test", "Audio_Test"),
        ("Test?Sound", "Test_Sound"),
        ("File*Name", "File_Name"),
        ("Path\\Test", "Path_Test"),
        ("Path/Test", "Path_Test"),
        ("CON", "user_CON"),  # Reserved name
        ("PRN", "user_PRN"),  # Reserved name
        ("", "recording"),    # Empty name
        ("   ", "recording"), # Whitespace only
        (".hidden", "hidden"), # Leading dot
        ("test.", "test"),     # Trailing dot
    ]
    
    all_passed = True
    for input_name, expected in test_cases:
        result = app.sanitize_filename(input_name)
        if result != expected:
            print(f"❌ FAIL: '{input_name}' -> '{result}' (expected '{expected}')")
            all_passed = False
        else:
            print(f"✅ PASS: '{input_name}' -> '{result}'")
    
    root.destroy()
    return all_passed

def test_platform_detection():
    """Test platform detection and Windows-specific features"""
    print("\nTesting platform detection...")
    
    system = platform.system()
    print(f"Detected platform: {system}")
    
    if system == "Windows":
        print("✅ Windows platform detected")
        
        # Test Windows version
        version = platform.version()
        print(f"Windows version: {version}")
        
        # Test if we can access Windows-specific modules
        try:
            import ctypes
            print("✅ ctypes module available for DPI awareness")
        except ImportError:
            print("❌ ctypes not available")
            
    else:
        print(f"ℹ️  Running on {system} (not Windows)")
    
    return True

def test_audio_device_detection():
    """Test audio device detection"""
    print("\nTesting audio device detection...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices")
        
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        print(f"Input devices: {len(input_devices)}")
        print(f"Output devices: {len(output_devices)}")
        
        if len(input_devices) == 0:
            print("⚠️  No input devices found - recording may not work")
            if platform.system() == "Windows":
                print("Windows tip: Check microphone permissions and device connections")
        else:
            print("✅ Input devices available")
            
        return True
        
    except Exception as e:
        print(f"❌ Audio device detection failed: {e}")
        return False

def test_file_operations():
    """Test file operations for Windows compatibility"""
    print("\nTesting file operations...")
    
    try:
        # Test directory creation
        test_dir = os.path.join(os.getcwd(), "test_recordings_windows")
        if not os.path.exists(test_dir):
            os.makedirs(test_dir, exist_ok=True)
            print("✅ Directory creation successful")
        
        # Test file writing with various names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_files = [
            f"test_user_{timestamp}.wav",
            f"user_with_spaces_{timestamp}.wav",
            f"unicode_test_héllo_{timestamp}.wav",
        ]
        
        for filename in test_files:
            filepath = os.path.join(test_dir, filename)
            try:
                # Create a dummy file
                with open(filepath, 'wb') as f:
                    f.write(b"test data")
                print(f"✅ File creation successful: {filename}")
                
                # Clean up
                os.remove(filepath)
                
            except Exception as e:
                print(f"❌ File creation failed for {filename}: {e}")
                return False
        
        # Clean up test directory
        os.rmdir(test_dir)
        print("✅ Cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_webcam_compatibility():
    """Test webcam and OpenCV compatibility on Windows"""
    print("\nTesting webcam and OpenCV compatibility...")
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        # Test webcam access
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam access successful")
            
            # Test basic properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"✅ Webcam resolution: {width}x{height}")
            
            # Test frame capture
            ret, frame = cap.read()
            if ret:
                print("✅ Frame capture successful")
            else:
                print("⚠️ Frame capture failed")
            
            cap.release()
        else:
            print("⚠️ No webcam detected or webcam in use")
        
        # Test video writer codecs
        codecs_to_test = ['mp4v', 'XVID', 'MJPG', 'WMV2']
        working_codecs = []
        
        for codec_name in codecs_to_test:
            try:
                fourcc = cv2.VideoWriter_fourcc(*codec_name)
                # Test with a dummy filename
                temp_path = os.path.join(os.getcwd(), f"test_{codec_name}.mp4")
                writer = cv2.VideoWriter(temp_path, fourcc, 30, (640, 480))
                if writer.isOpened():
                    working_codecs.append(codec_name)
                    writer.release()
                    # Clean up test file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            except:
                pass
        
        if working_codecs:
            print(f"✅ Working video codecs: {', '.join(working_codecs)}")
        else:
            print("❌ No working video codecs found")
        
        return len(working_codecs) > 0
        
    except ImportError:
        print("❌ OpenCV (cv2) not installed")
        print("   Try: pip install opencv-python")
        return False
    except Exception as e:
        print(f"❌ Webcam compatibility test failed: {e}")
        return False

def test_tkinter_compatibility():
    """Test tkinter GUI compatibility"""
    print("\nTesting tkinter compatibility...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test basic widgets
        frame = ttk.Frame(root)
        entry = ttk.Entry(frame)
        button = ttk.Button(frame, text="Test")
        progress = ttk.Progressbar(frame)
        
        print("✅ Basic tkinter widgets created successfully")
        
        # Test string variables
        var = tk.StringVar(value="test")
        entry.config(textvariable=var)
        
        print("✅ String variables working")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ tkinter compatibility test failed: {e}")
        return False

def main():
    """Run all Windows compatibility tests"""
    print("Windows Compatibility Test for Audio Recorder")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 50)
    
    tests = [
        ("Filename Sanitization", test_windows_filename_sanitization),
        ("Platform Detection", test_platform_detection),
        ("Audio Device Detection", test_audio_device_detection),
        ("File Operations", test_file_operations),
        ("Webcam Compatibility", test_webcam_compatibility),
        ("Tkinter Compatibility", test_tkinter_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The application should work well on Windows.")
        if platform.system() == "Windows":
            print("\nWindows-specific features:")
            print("- DPI awareness for high-resolution displays")
            print("- Windows filename sanitization")
            print("- Audio device permission checking")
            print("- Batch file for easy startup (run_windows.bat)")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Check the issues above.")
        
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
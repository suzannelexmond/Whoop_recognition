#!/usr/bin/env python3
"""
Basic test script to verify webcam functionality
without requiring GUI interaction.
"""

import cv2
import os
import tempfile
import time
from datetime import datetime

def test_webcam_availability():
    """Test if webcam is available and accessible"""
    print("Testing webcam availability...")
    
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam is available")
            cap.release()
            return True
        else:
            print("⚠️ No webcam detected or webcam is in use")
            return False
    except Exception as e:
        print(f"❌ Webcam test failed: {str(e)}")
        return False

def test_video_recording():
    """Test basic video recording functionality"""
    print("\nTesting video recording...")
    
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot open webcam for recording test")
            return False
        
        # Get webcam properties
        fps = 10  # Lower FPS for testing
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        
        # Create temporary test file
        test_dir = tempfile.mkdtemp()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"test_video_{timestamp}.mp4"
        video_filepath = os.path.join(test_dir, video_filename)
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))
        
        if not video_writer.isOpened():
            print("❌ Cannot initialize video writer")
            cap.release()
            return False
        
        # Record for 2 seconds (shorter than actual app)
        print("   Recording 2 seconds of test video...")
        start_time = time.time()
        frame_count = 0
        target_frames = fps * 2  # 2 seconds
        
        while time.time() - start_time < 2 and frame_count < target_frames:
            ret, frame = cap.read()
            if ret:
                video_writer.write(frame)
                frame_count += 1
            time.sleep(1.0 / fps)
        
        # Cleanup
        video_writer.release()
        cap.release()
        
        # Verify file exists and has content
        if os.path.exists(video_filepath) and os.path.getsize(video_filepath) > 0:
            file_size = os.path.getsize(video_filepath)
            print(f"✅ Test video recorded successfully: {video_filename} ({file_size} bytes)")
            
            # Clean up test file
            os.remove(video_filepath)
            os.rmdir(test_dir)
            print("✅ Cleanup completed")
            
            return True
        else:
            print("❌ Video file verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Video recording test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running basic webcam functionality tests...\n")
    
    test1 = test_webcam_availability()
    test2 = False
    
    if test1:
        test2 = test_video_recording()
    else:
        print("⚠️ Skipping video recording test due to webcam unavailability")
    
    print("\n" + "="*60)
    if test1 and test2:
        print("✅ All webcam tests passed! Video recording functionality should work.")
    elif test1 and not test2:
        print("⚠️ Webcam detected but video recording failed. Check OpenCV installation.")
    else:
        print("⚠️ No webcam available. Application will run in audio-only mode.")
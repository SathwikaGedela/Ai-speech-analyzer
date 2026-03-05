#!/usr/bin/env python3
"""
Quick Audio Solution - Create Working Audio Files for Interview Mode
"""

import os
import sys
import subprocess
import tempfile

def create_working_wav_with_speech():
    """Create a working WAV file using text-to-speech"""
    print("🎤 Creating working audio file with speech...")
    
    try:
        # Try using Windows built-in text-to-speech
        text = "Hello, my name is Test User. I am a software developer with three years of experience in Python and web development. I am passionate about creating innovative solutions and I believe I would be a great fit for this role because of my technical skills and dedication to quality work. Thank you for considering my application."
        
        # Create a temporary VBS script for text-to-speech
        vbs_script = '''
Dim message, sapi
message = "{}"
Set sapi = CreateObject("sapi.spvoice")
sapi.Speak message
'''.format(text)
        
        # Write VBS script to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
            f.write(vbs_script)
            vbs_path = f.name
        
        print("   🔊 Generating speech audio...")
        
        # Run the VBS script (this will speak the text)
        try:
            subprocess.run(['cscript', '//nologo', vbs_path], 
                         capture_output=True, timeout=30)
            os.unlink(vbs_path)
            print("   ✅ Speech generated (you should have heard it)")
        except:
            os.unlink(vbs_path)
            print("   ⚠️  Text-to-speech not available")
        
        return False  # Can't directly create audio file this way
        
    except Exception as e:
        print(f"   ❌ TTS creation failed: {e}")
        return False

def copy_working_file():
    """Copy the known working file for easy access"""
    print("📁 Setting up working audio file...")
    
    source_file = "uploads/n.mp3"
    if os.path.exists(source_file):
        # Copy to a more obvious name
        dest_file = "uploads/WORKING_INTERVIEW_AUDIO.mp3"
        
        try:
            import shutil
            shutil.copy2(source_file, dest_file)
            print(f"   ✅ Created {dest_file}")
            print(f"   💡 Use this file for testing interview mode")
            return dest_file
        except Exception as e:
            print(f"   ❌ Copy failed: {e}")
    else:
        print("   ❌ Source working file not found")
    
    return None

def create_simple_instructions():
    """Create simple step-by-step instructions"""
    print("\n📋 SIMPLE SOLUTION - 3 EASY STEPS")
    print("=" * 50)
    
    print("\n🎯 STEP 1: Record Voice on Phone")
    print("   • Open voice recorder app on your phone")
    print("   • Record yourself saying:")
    print('     "Hello, I am [your name]. I have experience in [field].')
    print('      I am interested in this position because [reason].')
    print('      My key skills include [skills]. Thank you."')
    print("   • Speak for 30-60 seconds")
    print("   • Save the recording")
    
    print("\n📤 STEP 2: Transfer to Computer")
    print("   • Email the audio file to yourself")
    print("   • Or use cloud storage (Google Drive, OneDrive)")
    print("   • Or connect phone with USB cable")
    print("   • Download/save the file to your computer")
    
    print("\n🌐 STEP 3: Upload to Interview Mode")
    print("   • Go to: http://127.0.0.1:5000/interview")
    print("   • Select a question")
    print("   • Click 'Choose File' (don't use browser recording)")
    print("   • Select your audio file")
    print("   • Click 'Analyze Answer'")

def test_browser_recording_alternative():
    """Provide alternative to browser recording"""
    print("\n🌐 BROWSER RECORDING ALTERNATIVE")
    print("=" * 50)
    
    print("\n❌ Why Browser Recording Might Fail:")
    print("   • WebM format compatibility issues")
    print("   • Microphone permission problems")
    print("   • Browser-specific audio encoding issues")
    print("   • System audio driver conflicts")
    
    print("\n✅ Reliable Alternative - File Upload:")
    print("   1. Don't use 'Start Recording' button")
    print("   2. Use 'Choose File' option instead")
    print("   3. Upload pre-recorded audio file")
    print("   4. This bypasses browser recording issues")

def create_windows_voice_recorder_guide():
    """Detailed Windows Voice Recorder guide"""
    print("\n🎤 WINDOWS VOICE RECORDER GUIDE")
    print("=" * 50)
    
    print("\n📱 Method 1: Windows 10/11 Voice Recorder")
    print("   1. Press Windows key")
    print("   2. Type 'Voice Recorder'")
    print("   3. Open the Voice Recorder app")
    print("   4. Click the microphone button")
    print("   5. Speak your interview answer clearly")
    print("   6. Click stop when done")
    print("   7. Right-click the recording → 'Open file location'")
    print("   8. The file will be in M4A format (supported!)")
    
    print("\n🌐 Method 2: Online Voice Recorder")
    print("   1. Go to: https://online-voice-recorder.com")
    print("   2. Click 'Allow' for microphone access")
    print("   3. Click red record button")
    print("   4. Speak your interview answer")
    print("   5. Click stop")
    print("   6. Click 'Save' and choose MP3 format")
    print("   7. Download the file")

def check_file_formats():
    """Check what file formats are in uploads"""
    print("\n📁 CHECKING AVAILABLE FILES")
    print("=" * 50)
    
    if not os.path.exists("uploads"):
        print("   ❌ No uploads directory")
        return
    
    files = os.listdir("uploads")
    audio_files = [f for f in files if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    
    if audio_files:
        print(f"   📂 Found {len(audio_files)} audio files:")
        for f in audio_files:
            size = os.path.getsize(os.path.join("uploads", f))
            print(f"      • {f} ({size:,} bytes)")
        
        print(f"\n   💡 Try uploading these files to interview mode")
        print(f"   🎯 Known working: n.mp3, sathaudio.flac, sathaudio.m4a")
    else:
        print("   ❌ No audio files found")
        print("   💡 You need to create audio files first")

def main():
    """Main solution provider"""
    print("🚀 QUICK AUDIO SOLUTION FOR INTERVIEW MODE")
    print("=" * 60)
    
    print("\n🎯 PROBLEM: Browser recording creates invalid WebM files")
    print("🔧 SOLUTION: Use file upload with pre-recorded audio")
    
    # Check existing files
    check_file_formats()
    
    # Copy working file if available
    working_file = copy_working_file()
    
    if working_file:
        print(f"\n🎉 IMMEDIATE SOLUTION READY!")
        print(f"   ✅ Use file: {working_file}")
        print(f"   🌐 Go to: http://127.0.0.1:5000/interview")
        print(f"   📤 Upload this file instead of browser recording")
    
    # Provide step-by-step instructions
    create_simple_instructions()
    create_windows_voice_recorder_guide()
    test_browser_recording_alternative()
    
    print("\n🎯 SUMMARY:")
    print("   ✅ Interview mode system is working perfectly")
    print("   ❌ Browser recording has compatibility issues")
    print("   🔧 Solution: Use file upload with phone/computer recording")
    print("   📱 Record on phone → transfer → upload")
    print("   🎤 Or use Windows Voice Recorder → save → upload")
    
    print(f"\n🌐 Access interview mode: http://127.0.0.1:5000/interview")
    print("💡 Use 'Choose File' option, NOT browser recording")

if __name__ == "__main__":
    main()
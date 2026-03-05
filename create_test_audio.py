#!/usr/bin/env python3
"""
Create Test Audio Files for Interview Mode
"""

import os
import sys

# Add backend to path
sys.path.append('backend')

def create_speech_like_audio():
    """Create a speech-like audio file for testing"""
    print("🎵 Creating speech-like test audio...")
    
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine, Square
        
        # Create speech-like patterns with varying frequencies
        segments = []
        
        # Simulate speech patterns with pauses
        frequencies = [200, 300, 400, 350, 250, 400, 300, 200]  # Speech-like frequency changes
        
        for i, freq in enumerate(frequencies):
            # Create tone segment
            tone = Sine(freq).to_audio_segment(duration=300)  # 300ms segments
            
            # Add some variation to make it more speech-like
            if i % 2 == 0:
                tone = tone.apply_gain(-10)  # Vary volume
            
            segments.append(tone)
            
            # Add pause between "words"
            if i < len(frequencies) - 1:
                pause = AudioSegment.silent(duration=100)  # 100ms pause
                segments.append(pause)
        
        # Combine all segments
        speech_like = sum(segments)
        
        # Apply overall gain reduction to make it more realistic
        speech_like = speech_like.apply_gain(-15)
        
        # Export as different formats
        formats = [
            ('test_speech.wav', 'wav'),
            ('test_speech.mp3', 'mp3'),
            ('test_speech.m4a', 'm4a')
        ]
        
        created_files = []
        
        for filename, format_name in formats:
            try:
                filepath = os.path.join('uploads', filename)
                os.makedirs('uploads', exist_ok=True)
                
                speech_like.export(filepath, format=format_name)
                print(f"   ✅ Created {filename} ({len(speech_like)/1000:.1f}s)")
                created_files.append(filepath)
                
            except Exception as e:
                print(f"   ❌ Failed to create {filename}: {e}")
        
        return created_files
        
    except ImportError:
        print("   ❌ pydub not available - cannot create test audio")
        return []
    except Exception as e:
        print(f"   ❌ Failed to create test audio: {e}")
        return []

def create_simple_wav():
    """Create a simple WAV file that should work"""
    print("\n🎵 Creating simple WAV file...")
    
    try:
        import wave
        import struct
        import math
        
        # Audio parameters
        sample_rate = 16000  # 16kHz sample rate
        duration = 3.0  # 3 seconds
        frequency = 440  # A4 note
        
        # Generate sine wave data
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            # Create a sine wave with some variation to simulate speech
            t = i / sample_rate
            
            # Mix multiple frequencies to simulate speech
            value = (
                0.3 * math.sin(2 * math.pi * frequency * t) +
                0.2 * math.sin(2 * math.pi * (frequency * 1.5) * t) +
                0.1 * math.sin(2 * math.pi * (frequency * 0.5) * t)
            )
            
            # Add some amplitude modulation to simulate speech patterns
            envelope = 0.5 + 0.5 * math.sin(2 * math.pi * 2 * t)  # 2Hz modulation
            value *= envelope
            
            # Convert to 16-bit integer
            sample = int(value * 32767)
            samples.append(sample)
        
        # Write WAV file
        filepath = os.path.join('uploads', 'simple_test.wav')
        os.makedirs('uploads', exist_ok=True)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Pack samples as binary data
            for sample in samples:
                wav_file.writeframes(struct.pack('<h', sample))
        
        print(f"   ✅ Created simple_test.wav ({duration}s)")
        return [filepath]
        
    except Exception as e:
        print(f"   ❌ Failed to create simple WAV: {e}")
        return []

def test_created_files(files):
    """Test the created audio files with interview mode"""
    print(f"\n🧪 Testing {len(files)} created audio files...")
    
    if not files:
        print("   ❌ No files to test")
        return False
    
    try:
        import requests
        
        url = "http://127.0.0.1:5000/interview/analyze"
        data = {
            'question': 'Tell me about yourself.',
            'category': 'hr'
        }
        
        for filepath in files:
            filename = os.path.basename(filepath)
            print(f"\n   🔧 Testing {filename}...")
            
            try:
                with open(filepath, 'rb') as f:
                    files_data = {'audio_file': (filename, f, 'audio/wav')}
                    response = requests.post(url, data=data, files=files_data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"      ✅ {filename} - SUCCESS!")
                        analysis = result.get('analysis', {})
                        print(f"         Confidence: {analysis.get('confidence', 'N/A')}")
                        print(f"         WPM: {analysis.get('metrics', {}).get('wpm', 'N/A')}")
                        return True
                    else:
                        error = result.get('error', 'Unknown')
                        print(f"      ❌ {filename} - Analysis failed: {error}")
                else:
                    print(f"      ❌ {filename} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ {filename} - Exception: {e}")
        
        return False
        
    except ImportError:
        print("   ❌ requests not available - cannot test files")
        return False
    except Exception as e:
        print(f"   ❌ Testing failed: {e}")
        return False

def check_existing_working_files():
    """Check if there are existing working files"""
    print("📁 Checking existing audio files...")
    
    if not os.path.exists('uploads'):
        print("   ❌ No uploads directory")
        return []
    
    working_files = []
    
    # Check files that worked in previous tests
    known_working = ['n.mp3', 'sathaudio.flac', 'sathaudio.m4a']
    
    for filename in known_working:
        filepath = os.path.join('uploads', filename)
        if os.path.exists(filepath):
            print(f"   ✅ Found working file: {filename}")
            working_files.append(filepath)
    
    return working_files

def provide_user_guidance():
    """Provide guidance for users experiencing audio issues"""
    print("\n💡 USER GUIDANCE FOR AUDIO ISSUES")
    print("=" * 50)
    
    print("\n🎤 If Browser Recording Fails:")
    print("   1. Check microphone permissions in browser")
    print("   2. Try a different browser (Chrome works best)")
    print("   3. Ensure microphone is not being used by other apps")
    print("   4. Speak clearly and loudly")
    print("   5. Record in a quiet environment")
    
    print("\n📁 If File Upload Fails:")
    print("   1. Use WAV, MP3, M4A, or FLAC formats")
    print("   2. Ensure file contains actual speech (not music)")
    print("   3. Keep file size under 16MB")
    print("   4. Try converting file to WAV format")
    print("   5. Record with phone voice recorder and upload")
    
    print("\n🔧 Quick Solutions:")
    print("   • Use phone voice recorder app → save as WAV → upload")
    print("   • Try Audacity to record and export as WAV")
    print("   • Use Windows Voice Recorder → save → upload")
    print("   • Record a simple 'Hello, this is a test' message")
    
    print("\n✅ What Should Work:")
    print("   • Clear speech in quiet environment")
    print("   • 30 seconds to 2 minutes duration")
    print("   • WAV format (most reliable)")
    print("   • Speaking at normal conversational pace")

def main():
    """Create test audio files and provide guidance"""
    print("🎵 Audio File Creator for Interview Mode")
    print("=" * 50)
    
    # Check existing files first
    existing_files = check_existing_working_files()
    
    if existing_files:
        print(f"\n✅ Found {len(existing_files)} existing working files")
        print("💡 Try using these files first:")
        for filepath in existing_files:
            print(f"   - {os.path.basename(filepath)}")
    
    # Create new test files
    print("\n🔧 Creating new test audio files...")
    
    created_files = []
    
    # Try creating speech-like audio with pydub
    pydub_files = create_speech_like_audio()
    created_files.extend(pydub_files)
    
    # Create simple WAV file
    wav_files = create_simple_wav()
    created_files.extend(wav_files)
    
    if created_files:
        print(f"\n✅ Created {len(created_files)} test audio files")
        
        # Test the created files
        success = test_created_files(created_files)
        
        if success:
            print("\n🎉 SUCCESS! Test audio files work with interview mode")
            print("💡 You can now use these files to test interview mode")
        else:
            print("\n⚠️  Test files created but may need real speech content")
    
    # Provide user guidance
    provide_user_guidance()
    
    print(f"\n🌐 Access interview mode at: http://127.0.0.1:5000/interview")

if __name__ == "__main__":
    main()
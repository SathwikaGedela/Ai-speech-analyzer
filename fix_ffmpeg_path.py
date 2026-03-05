"""
Fix FFmpeg path issue for the current session
Run this before starting the Flask app
"""

import os
import subprocess

def find_and_set_ffmpeg():
    """Find FFmpeg installation and set it in PATH"""
    
    print("🔍 Looking for FFmpeg installation...")
    
    # Common FFmpeg installation paths on Windows
    possible_paths = [
        r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin"
    ]
    
    # Check each path
    for path in possible_paths:
        ffmpeg_exe = os.path.join(path, "ffmpeg.exe")
        if os.path.exists(ffmpeg_exe):
            print(f"✅ Found FFmpeg at: {path}")
            
            # Add to current session PATH
            current_path = os.environ.get("PATH", "")
            if path not in current_path:
                os.environ["PATH"] = current_path + os.pathsep + path
                print(f"✅ Added to PATH: {path}")
            
            # Test if it works
            try:
                result = subprocess.run([ffmpeg_exe, "-version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print("✅ FFmpeg is working!")
                    return True
                else:
                    print("❌ FFmpeg found but not working properly")
            except Exception as e:
                print(f"❌ Error testing FFmpeg: {e}")
            
            break
    else:
        print("❌ FFmpeg not found in common locations")
        return False
    
    return True

def set_pydub_ffmpeg_path():
    """Set FFmpeg path specifically for pydub"""
    
    try:
        from pydub import AudioSegment
        from pydub.utils import which
        
        # Check if FFmpeg is already available
        if which("ffmpeg"):
            print("✅ FFmpeg already available to pydub")
            return True
        
        # Set explicit path for pydub
        ffmpeg_path = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
        
        if os.path.exists(os.path.join(ffmpeg_path, "ffmpeg.exe")):
            AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
            AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
            AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
            
            print("✅ Set explicit FFmpeg path for pydub")
            return True
        else:
            print("❌ FFmpeg executable not found")
            return False
            
    except ImportError:
        print("❌ pydub not installed")
        return False
    except Exception as e:
        print(f"❌ Error setting pydub FFmpeg path: {e}")
        return False

if __name__ == "__main__":
    print("🔧 FFmpeg Path Fix Utility")
    print("=" * 30)
    
    # Try to find and set FFmpeg
    path_ok = find_and_set_ffmpeg()
    pydub_ok = set_pydub_ffmpeg_path()
    
    print("\n" + "=" * 30)
    if path_ok and pydub_ok:
        print("🎉 FFmpeg setup complete!")
        print("You can now run: python app.py")
        print("MP3 files should work properly.")
    else:
        print("⚠️  FFmpeg setup incomplete.")
        print("Consider using WAV files instead of MP3.")
        print("Or convert MP3 to WAV using online tools.")
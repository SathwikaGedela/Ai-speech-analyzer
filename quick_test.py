"""
Quick test after restarting terminal
"""
import subprocess
import sys

def test_ffmpeg_command():
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is working!")
            print("First few lines of output:")
            print(result.stdout.split('\n')[0])
            return True
        else:
            print("❌ FFmpeg command failed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error testing FFmpeg: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Quick FFmpeg Test")
    print("-" * 20)
    test_ffmpeg_command()
    print("\nIf this fails, please restart your terminal and try again.")
import os
import shutil
from pydub import AudioSegment
from werkzeug.utils import secure_filename

AUDIO_DIR = "uploads"

# Global FFmpeg setup - run once when module is imported
def setup_ffmpeg():
    """Setup FFmpeg path detection"""
    # Try multiple common FFmpeg locations
    ffmpeg_paths = [
        # WinGet installation (correct path)
        r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        # System PATH - try to get from which command
        shutil.which("ffmpeg"),
        # Common installation paths
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin"
    ]
    
    for path in ffmpeg_paths:
        if path:
            if os.path.isfile(path):
                # If it's the executable file, get the directory
                ffmpeg_dir = os.path.dirname(path)
                ffmpeg_exe = path
            else:
                # If it's a directory, look for ffmpeg.exe inside
                ffmpeg_dir = path
                ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
            
            if os.path.exists(ffmpeg_exe):
                AudioSegment.converter = ffmpeg_exe
                AudioSegment.ffmpeg = ffmpeg_exe
                ffprobe_exe = os.path.join(ffmpeg_dir, "ffprobe.exe")
                if os.path.exists(ffprobe_exe):
                    AudioSegment.ffprobe = ffprobe_exe
                print(f"✅ FFmpeg found and configured at: {ffmpeg_dir}")
                return True
    
    print("❌ FFmpeg not found - some audio formats may not work")
    return False

# Setup FFmpeg immediately when module is imported
FFMPEG_AVAILABLE = setup_ffmpeg()

def process_audio(file):
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
    
    filename = secure_filename(file.filename)
    path = os.path.join(AUDIO_DIR, filename)
    file.save(path)
    
    # Ensure FFmpeg is configured (redundant check for safety)
    if not FFMPEG_AVAILABLE:
        print("⚠️  FFmpeg not available, re-attempting setup...")
        ffmpeg_available = setup_ffmpeg()
    else:
        ffmpeg_available = FFMPEG_AVAILABLE
    
    try:
        # Handle different audio formats
        if filename.lower().endswith(".wav"):
            # WAV files can be processed directly
            audio = AudioSegment.from_wav(path)
        elif filename.lower().endswith(".mp3"):
            if not ffmpeg_available:
                raise Exception("MP3 files require FFmpeg. Please use WAV format or install FFmpeg.")
            audio = AudioSegment.from_mp3(path)
            wav_path = path.replace(".mp3", ".wav")
            audio.export(wav_path, format="wav")
            path = wav_path
        elif filename.lower().endswith(".m4a"):
            if not ffmpeg_available:
                raise Exception("M4A files require FFmpeg. Please use WAV format or install FFmpeg.")
            audio = AudioSegment.from_file(path, format="m4a")
            wav_path = path.replace(".m4a", ".wav")
            audio.export(wav_path, format="wav")
            path = wav_path
        elif filename.lower().endswith(".flac"):
            if not ffmpeg_available:
                raise Exception("FLAC files require FFmpeg. Please use WAV format or install FFmpeg.")
            audio = AudioSegment.from_file(path, format="flac")
            wav_path = path.replace(".flac", ".wav")
            audio.export(wav_path, format="wav")
            path = wav_path
        elif filename.lower().endswith(".webm"):
            if not ffmpeg_available:
                raise Exception("WebM files require FFmpeg. Please use WAV format or install FFmpeg.")
            audio = AudioSegment.from_file(path, format="webm")
            wav_path = path.replace(".webm", ".wav")
            audio.export(wav_path, format="wav", parameters=["-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1"])
            path = wav_path
        else:
            # Try to process as generic audio file
            if not ffmpeg_available:
                raise Exception(f"Unknown audio format '{filename}' requires FFmpeg. Please use WAV format or install FFmpeg.")
            audio = AudioSegment.from_file(path)
            if not filename.lower().endswith(".wav"):
                wav_path = os.path.splitext(path)[0] + ".wav"
                audio.export(wav_path, format="wav")
                path = wav_path
        
        # Get duration
        if not 'audio' in locals():
            audio = AudioSegment.from_wav(path)
        duration = len(audio) / 1000.0  # Convert to seconds
        
        print(f"✅ Audio processed successfully: {filename} ({duration:.1f}s)")
        return path, duration
        
    except Exception as e:
        # Clean up the uploaded file on error
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass
        
        error_msg = str(e)
        print(f"❌ Audio processing error: {error_msg}")
        
        # Provide more specific error messages based on the actual error
        if "EBML header parsing failed" in error_msg or "Invalid data found" in error_msg:
            raise Exception("Invalid or corrupted audio file. Please try recording again or upload a different audio file.")
        elif "ffmpeg returned error code" in error_msg:
            if filename.lower().endswith(".webm"):
                raise Exception("WebM file processing failed. This might be due to browser recording issues. Please try recording again or upload a WAV/MP3 file instead.")
            else:
                raise Exception(f"Audio file '{filename}' appears to be corrupted or in an unsupported format. Please try a different file or convert to WAV/MP3 format.")
        elif "ffmpeg" in error_msg.lower() or not ffmpeg_available:
            raise Exception("FFmpeg is required for this audio format. Please ensure FFmpeg is installed or try uploading a WAV file instead.")
        else:
            raise Exception(f"Could not process audio file '{filename}': {error_msg}")
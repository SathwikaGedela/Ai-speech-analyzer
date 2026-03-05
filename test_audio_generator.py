"""
Simple script to generate test audio files for the speech feedback system
This is for testing purposes when you don't have audio files ready
"""

import pyttsx3
import os

def generate_test_audio():
    """Generate sample audio files for testing"""
    
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Sample speeches for testing
    test_speeches = {
        'fast_speech.wav': "Hello everyone, I am very excited to be here today to talk about artificial intelligence and machine learning. These technologies are revolutionizing the way we work and live. They are changing everything from healthcare to transportation to education. The possibilities are endless and the future is bright.",
        
        'slow_speech.wav': "Hello... everyone. I am... very excited... to be here... today. I want to... talk about... artificial intelligence... and... machine learning.",
        
        'filler_heavy.wav': "Um, hello everyone. So, like, I am, uh, very excited to be here today. You know, I want to, um, talk about, like, artificial intelligence and, uh, machine learning. So, basically, these technologies are, um, really changing everything.",
        
        'confident_speech.wav': "Good morning everyone! I am thrilled to be here today to share my passion for artificial intelligence and machine learning. These incredible technologies are transforming our world in amazing ways. From revolutionizing healthcare to advancing education, AI is creating endless opportunities for innovation and growth."
    }
    
    print("Generating test audio files...")
    
    for filename, text in test_speeches.items():
        filepath = os.path.join('uploads', filename)
        print(f"Creating {filename}...")
        
        # Save to file
        engine.save_to_file(text, filepath)
    
    # Process the queue
    engine.runAndWait()
    
    print("Test audio files generated successfully!")
    print("Files created in 'uploads' folder:")
    for filename in test_speeches.keys():
        print(f"  - {filename}")

if __name__ == "__main__":
    try:
        generate_test_audio()
    except Exception as e:
        print(f"Error generating audio files: {e}")
        print("You may need to install pyttsx3: pip install pyttsx3")
        print("Or you can use your own audio files for testing.")
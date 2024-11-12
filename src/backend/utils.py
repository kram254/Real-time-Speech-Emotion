import wave
import os
import subprocess
from src.backend.config import DATA_DIR

def save_audio(audio_bytes, sample_width, sample_rate, num_channels=1):
    """
    Saves audio bytes to a fixed WAV file: data/output.wav
    """
    try:
        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Define the fixed filename
        filename = "output.wav"
        abs_audio_path = os.path.join(DATA_DIR, filename)
        
        print(f"Saving audio to: {abs_audio_path}")
        print(f"Audio parameters - Width: {sample_width}, Rate: {sample_rate}, Channels: {num_channels}")
        
        # Write the audio bytes to the WAV file
        with wave.open(abs_audio_path, 'wb') as wave_file:
            wave_file.setnchannels(num_channels)
            wave_file.setsampwidth(sample_width)
            wave_file.setframerate(sample_rate)
            wave_file.writeframes(audio_bytes)
        
        # Verify that the file was created successfully
        if os.path.exists(abs_audio_path):
            file_size = os.path.getsize(abs_audio_path)
            print(f"Audio file saved successfully. Size: {file_size} bytes")
            print(f"Absolute path: {abs_audio_path}")
            if file_size == 0:
                print("Warning: The saved audio file is empty.")
                raise ValueError("Saved audio file is empty.")
            return abs_audio_path
        else:
            print(f"Warning: Audio file was not created at {abs_audio_path}")
            raise FileNotFoundError(f"Audio file was not created at {abs_audio_path}")
            
    except Exception as e:
        print(f"Error in save_audio: {str(e)}")
        raise

def verify_audio_file(audio_path):
    """
    Verifies the integrity of the audio file using FFmpeg.
    """
    try:
        result = subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', audio_path, '-f', 'null', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print("Audio file verification successful.")
        else:
            print("Audio file verification failed.")
            print(result.stderr)
            raise ValueError("FFmpeg verification failed.")
    except Exception as e:
        print(f"Error verifying audio file with FFmpeg: {e}")
        raise

def get_sentiment_emoji(sentiment):
    """
    Maps sentiment labels to corresponding emojis.
    """
    emoji_mapping = {
        "disappointment": "😞",
        "sadness": "😢",
        "annoyance": "😠",
        "neutral": "😐",
        "disapproval": "👎",
        "realization": "😮",
        "nervousness": "😬",
        "approval": "👍",
        "joy": "😄",
        "anger": "😡",
        "embarrassment": "😳",
        "caring": "🤗",
        "remorse": "😔",
        "disgust": "🤢",
        "grief": "😥",
        "confusion": "😕",
        "relief": "😌",
        "desire": "😍",
        "admiration": "😌",
        "optimism": "😊",
        "fear": "😨",
        "love": "❤️",
        "excitement": "🎉",
        "curiosity": "🤔",
        "amusement": "😄",
        "surprise": "😲",
        "gratitude": "🙏",
        "pride": "🦁"
    }
    return emoji_mapping.get(sentiment, "")
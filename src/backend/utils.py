import wave
import os
import subprocess
from src.backend.config import DATA_DIR



def save_audio(audio_bytes, sample_width, sample_rate, num_channels=1):
    """
    Saves the recorded audio bytes directly to the data directory
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        abs_audio_path = os.path.join(DATA_DIR, "recorded_audio.wav")
        
        # Write the audio bytes directly to file
        with open(abs_audio_path, 'wb') as f:
            f.write(audio_bytes)
        
        # Verify the file
        if os.path.exists(abs_audio_path):
            file_size = os.path.getsize(abs_audio_path)
            print(f"Audio file saved successfully. Size: {file_size} bytes")
            if file_size == 0:
                raise ValueError("Saved audio file is empty")
            return abs_audio_path
        else:
            raise FileNotFoundError(f"Failed to save audio file at {abs_audio_path}")
            
    except Exception as e:
        print(f"Error saving audio: {str(e)}")
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
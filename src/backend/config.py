import os

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')  

# # Audio File Path
# TEMP_AUDIO_FILE = os.path.join(DATA_DIR, 'output.wav')

# Model Names
WHISPER_MODEL_NAME = "small"
SENTIMENT_MODEL_NAME = "SamLowe/roberta-base-go_emotions"

# Audio File Path
TEMP_AUDIO_FILE = os.path.join(DATA_DIR, 'recorded_audio.wav')
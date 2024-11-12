import whisper
from transformers import pipeline
from src.backend.config import WHISPER_MODEL_NAME, SENTIMENT_MODEL_NAME
import os

class Models:
    def __init__(self):
        self.whisper_model = self.load_whisper_model()
        self.sentiment_pipeline = self.load_sentiment_pipeline()
    
    def load_whisper_model(self):
        """
        Loads the Whisper ASR model.
        """
        model = whisper.load_model(WHISPER_MODEL_NAME)
        print(f"{WHISPER_MODEL_NAME.capitalize()} Whisper Model Loaded!")
        return model
    
    def load_sentiment_pipeline(self):
        """
        Loads the sentiment analysis pipeline.
        """
        sentiment = pipeline("sentiment-analysis", framework="pt", model=SENTIMENT_MODEL_NAME)
        print("Sentiment Analysis Pipeline Loaded!")
        return sentiment
    
    def transcribe_audio(self, audio_path):
        """
        Transcribes audio to text using Whisper.
        """
        try:
            print(f"Attempting to transcribe audio file: {audio_path}")
            if not os.path.exists(audio_path):
                print(f"Audio file does not exist: {audio_path}")
                raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

            file_size = os.path.getsize(audio_path)
            print(f"Audio file size: {file_size} bytes")
            if file_size == 0:
                print("Audio file is empty. Cannot transcribe.")
                raise ValueError("Audio file is empty.")

            # Transcribe with additional parameters for better accuracy
            result = self.whisper_model.transcribe(audio_path, language="en")  # Specify language if known
            print("Transcription complete.")
            return result.get("text", "")
        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
            raise
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            raise
    
    def analyze_sentiment(self, text):
        """
        Analyzes sentiment of the given text.
        """
        if not text.strip():
            print("No text provided for sentiment analysis.")
            return {"neutral": 1.0}
        results = self.sentiment_pipeline(text)
        sentiment_results = {result['label'].lower(): result['score'] for result in results}
        return sentiment_results
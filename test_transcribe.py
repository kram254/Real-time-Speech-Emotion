import whisper
import os

def test_transcription(audio_path):
    if not os.path.exists(audio_path):
        print(f"Audio file does not exist: {audio_path}")
        return

    model = whisper.load_model("base")
    try:
        print(f"Transcribing audio file: {audio_path}")
        result = model.transcribe(audio_path)
        print("Transcription:", result["text"])
    except Exception as e:
        print(f"Error during transcription: {e}")

if __name__ == "__main__":
    audio_path = r"D:\Codex Home\Real-time Speech Emotion\src\data\output.wav"
    test_transcription(audio_path)
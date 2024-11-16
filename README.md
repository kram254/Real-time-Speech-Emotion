# Real-time Speech Emotion Recognition

![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

## Overview

This project aims to develop a real-time speech emotion recognition system that accurately detects emotions from audio inputs. Leveraging advanced machine learning algorithms and feature extraction techniques, the system transcribes speech and analyzes sentiments to enhance human-computer interaction through emotional intelligence.

## Features

- **Real-time Audio Recording**: Users can record their voice directly from the web interface.
- **Speech-to-Text Transcription**: Utilizes OpenAI's Whisper model for accurate transcription.
- **Sentiment Analysis**: Analyzes the transcribed text to identify emotions.
- **Interactive UI**: Built with Streamlit, featuring progress indicators and customizable sentiment display options.
- **Emotion Emojis**: Visual representation of detected emotions using emojis.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/real-time-speech-emotion-recognition.git
   cd real-time-speech-emotion-recognition
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   streamlit run src/frontend/app.py
   ```

## Usage

1. Open the Streamlit app in your browser.
2. Click the record button to start recording your voice.
3. Click the stop button to finish recording.
4. Select the sentiment analysis options (e.g., Sentiments, Sentiments with Scores).
5. Click the "Get Sentiments" button to view the analysis.


# Data files
data/recorded_audio.wav


## Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building the interactive web UI.
- **[OpenAI Whisper](https://github.com/openai/whisper)**: For speech-to-text transcription.
- **[Transformers](https://huggingface.co/transformers/)**: For sentiment analysis.
- **[Streamlit Mic Recorder](https://github.com/ravishanker86/streamlit-mic-recorder)**: For audio recording in the browser.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

[MIT](LICENSE)

## Acknowledgements

- [OpenAI](https://openai.com/) for the Whisper model.
- [Hugging Face](https://huggingface.co/) for the Transformers library.
import streamlit as st
from src.backend.models import Models
from src.backend.utils import save_audio, get_sentiment_emoji, verify_audio_file
import os
import time
from streamlit_mic_recorder import mic_recorder

def main():
    try:
        # Initialize directories and configuration
        from src.backend.config import DATA_DIR, TEMP_AUDIO_FILE

        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Data directory ensured at: {DATA_DIR}")

        # Initialize Models
        models = Models()

        # Streamlit App Structure
        st.set_page_config(
            page_title="🎤 Real-time Speech Emotion Recognition",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        st.title("🎤 Real-time Speech Emotion Recognition 💬")

        # Load Custom CSS
        def local_css(file_name):
            try:
                with open(file_name) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                print(f"Loaded CSS from: {file_name}")
            except Exception as e:
                st.warning(f"Could not load CSS file: {str(e)}")
                print(f"Failed to load CSS file: {str(e)}")

        css_path = os.path.join(os.path.dirname(__file__), '../assets/styles.css')
        if os.path.exists(css_path):
            local_css(css_path)
        else:
            st.warning("CSS file does not exist.")
            print(f"CSS file not found at: {css_path}")

        st.write("Record your voice, and analyze the emotions!")

        # Audio Recording
        try:
            audio = mic_recorder(
                start_prompt="⏺️ Click to start recording",
                stop_prompt="⏹️ Click to stop recording",
                key="recorder"
            )
            print("Audio recording attempted.")
        except Exception as e:
            st.error(f"Error accessing microphone: {str(e)}")
            print(f"Microphone error details: {str(e)}")
            return

        if audio:
            try:
                audio_bytes = audio.get('bytes')
                if not audio_bytes:
                    st.error("No audio data received from the recorder.")
                    print("No audio bytes received.")
                    return

                # Debugging: Log the size of audio bytes
                print(f"Received audio bytes of length: {len(audio_bytes)}")

                st.audio(audio_bytes, format='audio/wav')

                # Save the recorded audio to data/output.wav
                sample_width = audio.get("sample_width", 2)    # Default to 2 bytes if not provided
                sample_rate = audio.get("sample_rate", 44100)  # Default to 44100 Hz if not provided
                num_channels = audio.get("num_channels", 1)    # Default to mono if not provided

                abs_audio_path = save_audio(
                    audio_bytes=audio_bytes,
                    sample_width=sample_width,
                    sample_rate=sample_rate,
                    num_channels=num_channels
                )

                print(f"Audio saved successfully to: {abs_audio_path}")

                # Verify the audio file with FFmpeg
                verify_audio_file(abs_audio_path)

                # Store the absolute path in session state
                st.session_state['audio_path'] = abs_audio_path
                print(f"Audio path stored in session state: {abs_audio_path}")
                
            except Exception as e:
                st.error(f"Error saving audio: {str(e)}")
                print(f"Audio saving error details: {str(e)}")
                return

        # Sentiment Options
        st.subheader("Select Sentiment Analysis Options")
        sentiment_options = st.multiselect(
            "Choose the sentiment options you want to display:",
            ["Sentiments", "Sentiments with Points"],
            default=["Sentiments"]
        )

        # Button to Trigger Processing
        if st.button("Get Sentiments"):
            audio_path = st.session_state.get('audio_path', TEMP_AUDIO_FILE)
            print(f"Retrieved audio path from session state: {audio_path}")
            if not os.path.exists(audio_path):
                st.error(f"Audio file not found at: {audio_path}")
                print(f"Missing audio file at path: {audio_path}")
            else:
                try:
                    file_size = os.path.getsize(audio_path)
                    print(f"Audio file size before processing: {file_size} bytes")
                    if file_size == 0:
                        st.error("Audio file is empty. Please record audio again.")
                        print("Audio file is empty.")
                        return

                    print(f"Starting processing of audio file: {audio_path}")
                    with st.spinner("Processing..."):
                        # Transcribe Audio
                        transcription = models.transcribe_audio(audio_path)
                        print("Transcription:", transcription)  # Log the transcription
                        st.success("Transcription Complete!")
                        st.write("**Transcribed Text:**")
                        st.write(transcription)
                        
                        # Analyze Sentiment
                        sentiment_results = models.analyze_sentiment(transcription)
                        print(f"Sentiment analysis results: {sentiment_results}")
                        
                        # Display Progress Bar
                        progress_placeholder = st.empty()
                        progress_text = st.empty()
                        progress_bar = progress_placeholder.progress(0)
                        
                        for percent in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(percent + 1)
                            progress_text.text(f"Analyzing sentiments... {percent + 1}%")
                        
                        progress_placeholder.empty()
                        progress_text.empty()
                        st.success("Sentiment Analysis Complete!")

                        # Display Results
                        st.write("**Sentiment Results:**")
                        for sentiment, score in sentiment_results.items():
                            emoji = get_sentiment_emoji(sentiment)
                            if "Sentiments with Points" in sentiment_options:
                                st.write(f"{sentiment} {emoji}: {score:.2f}")
                            else:
                                st.write(f"{sentiment} {emoji}")
                
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                    print(f"Processing error details: {str(e)}")

        # Footer
        st.markdown('''
            ---
            Whisper Model by [OpenAI](https://github.com/openai/whisper) | 
            Sentiment Analysis by [SamLowe](https://huggingface.co/SamLowe/roberta-base-go_emotions)
        ''')

    except Exception as e:
        st.error(f"Failed to initialize application: {e}")
        print(f"Application initialization error: {str(e)}")
        return

if __name__ == '__main__':
    main()




























# import streamlit as st
# from src.backend.models import Models
# from src.backend.utils import save_audio, get_sentiment_emoji
# import wave
# import os
# import time
# import sys
# from streamlit_mic_recorder import mic_recorder
# import subprocess

# def init_directories():
#     """Initialize required directories"""
#     from src.backend.config import DATA_DIR, BASE_DIR, MODEL_DIR
#     directories = [DATA_DIR, MODEL_DIR]
#     for directory in directories:
#         try:
#             os.makedirs(directory, exist_ok=True)
#             print(f"Directory created/verified: {directory}")
#         except Exception as e:
#             print(f"Error creating directory {directory}: {str(e)}")
            
# def check_ffmpeg():
#     try:
#         result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if result.returncode == 0:
#             print("FFmpeg is installed and accessible.")
#             print(result.stdout)
#         else:
#             print("FFmpeg is not accessible.")
#             print(result.stderr)
#     except FileNotFoundError:
#         print("FFmpeg executable not found. Please ensure FFmpeg is installed and added to PATH.")

# def verify_audio_file(audio_path):
#     try:
#         result = subprocess.run(['ffmpeg', '-i', audio_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if result.returncode == 0:
#             print("Audio file verification successful.")
#         else:
#             print("Audio file verification failed.")
#             print(result.stderr)
#     except Exception as e:
#         print(f"Error verifying audio file with FFmpeg: {e}")

# def main():
#     check_ffmpeg()
#     print("Current PATH:", os.environ.get('PATH'))
#     try:
#         # Initialize directories
#         init_directories()
        
#         # Initialize Models
#         models = Models()

#         # Configuration
#         from src.backend.config import TEMP_AUDIO_FILE
#         print(f"Audio file will be saved to: {TEMP_AUDIO_FILE}")

#         # Streamlit App Structure
#         st.set_page_config(
#             page_title="🎤 Real-time Speech Emotion Recognition",
#             layout="centered",
#             initial_sidebar_state="collapsed"
#         )
#         st.title("🎤 Real-time Speech Emotion Recognition 💬")

#         # Load Custom CSS
#         def local_css(file_name):
#             try:
#                 with open(file_name) as f:
#                     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#             except Exception as e:
#                 st.warning(f"Could not load CSS file: {str(e)}")

#         css_path = os.path.join(os.path.dirname(__file__), '../assets/styles.css')
#         if os.path.exists(css_path):
#             local_css(css_path)

#         st.write("Record your voice, and analyze the emotions!")

#         # Audio Recording
#         try:
#             audio = mic_recorder(
#                 start_prompt="Click to start recording",
#                 stop_prompt="Click to stop recording",
#                 key="recorder"
#             )
#         except Exception as e:
#             st.error(f"Error accessing microphone: {str(e)}")
#             print(f"Microphone error details: {str(e)}")
#             return

#         if audio:
#             try:
#                 audio_bytes = audio['bytes']
#                 st.audio(audio_bytes)
#                 print(f"Audio recorded successfully, length: {len(audio_bytes)} bytes")
                
#                 # Save the recorded audio
#                 sample_width = 2
#                 sample_rate = 44100
#                 num_channels = 1

#                 abs_audio_path = save_audio(audio_bytes, sample_width, sample_rate, num_channels)
#                 print(f"Audio saved successfully to: {abs_audio_path}")

#                 # Verify the audio file with FFmpeg
#                 verify_audio_file(abs_audio_path)

#                 # Store the absolute path in session state
#                 st.session_state['audio_path'] = abs_audio_path
                
#             except Exception as e:
#                 st.error(f"Error saving audio: {str(e)}")
#                 print(f"Audio saving error details: {str(e)}")
#                 return

#         # Sentiment Options
#         st.subheader("Select Sentiment Analysis Options")
#         sentiment_options = st.multiselect(
#             "Choose the sentiment options you want to display:",
#             ["Sentiments", "Sentiments with Points"],
#             default=["Sentiments"]
#         )

#         # Button to Trigger Processing
#         if st.button("Get Sentiments"):
#             audio_path = st.session_state.get('audio_path', TEMP_AUDIO_FILE)
#             if not os.path.exists(audio_path):
#                 st.error(f"Audio file not found at: {audio_path}")
#                 print(f"Missing audio file at path: {audio_path}")
#             else:
#                 try:
#                     print(f"Starting processing of audio file: {audio_path}")
#                     with st.spinner("Processing..."):
#                         # Transcribe Audio
#                         transcription = models.transcribe_audio(audio_path)
#                         print("Transcription:", transcription)  # Log the transcription
#                         st.success("Transcription Complete!")
#                         st.write("**Transcribed Text:**")
#                         st.write(transcription)
                        
#                         # Analyze Sentiment
#                         sentiment_results = models.analyze_sentiment(transcription)
#                         print(f"Sentiment analysis results: {sentiment_results}")
                        
#                         # Display Progress Bar
#                         progress_placeholder = st.empty()
#                         progress_text = st.empty()
#                         progress_bar = progress_placeholder.progress(0)
                        
#                         for percent in range(100):
#                             time.sleep(0.01)
#                             progress_bar.progress(percent + 1)
#                             progress_text.text(f"Analyzing sentiments... {percent + 1}%")
                        
#                         progress_placeholder.empty()
#                         progress_text.empty()
#                         st.success("Sentiment Analysis Complete!")

#                         # Display Results
#                         st.write("**Sentiment Results:**")
#                         for sentiment, score in sentiment_results.items():
#                             emoji = get_sentiment_emoji(sentiment)
#                             if "Sentiments with Points" in sentiment_options:
#                                 st.write(f"{sentiment} {emoji}: {score:.2f}")
#                             else:
#                                 st.write(f"{sentiment} {emoji}")
                            
#                 except Exception as e:
#                     st.error(f"Error processing audio: {str(e)}")
#                     print(f"Processing error details: {str(e)}")

#         # Footer
#         st.markdown('''
#             ---
#             Whisper Model by [OpenAI](https://github.com/openai/whisper) | 
#             Sentiment Analysis by [SamLowe](https://huggingface.co/SamLowe/roberta-base-go_emotions)
#         ''')

#     except Exception as e:
#         st.error(f"Failed to initialize application: {e}")
#         print(f"Application initialization error: {str(e)}")
#         return

# if __name__ == '__main__':
#     main()
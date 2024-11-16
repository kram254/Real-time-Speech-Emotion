import streamlit as st
from src.backend.models import Models
from src.backend.utils import save_audio, get_sentiment_emoji, verify_audio_file
import os

from streamlit_mic_recorder import mic_recorder
from PIL import Image

def main():
    # Set page configuration with wide layout, custom title, and icon
    st.set_page_config(
        page_title="🎤 Real-time Speech Emotion Recognition",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide Streamlit's default menu and footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("Real-time Speech Emotion Recognition 💬")

    # Add custom CSS
    st.markdown(
        f"""
        <style>
        .main {{
            background-color: #f0f2f6;
        }}
        h1 {{
            color: #4B8BBE;
            text-align: center;
        }}
        .button-record {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }}
        .progress-bar {{
            background-color: #4CAF50;
            height: 20px;
            width: 0%;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize Models
    models = Models()
    
    # Create a container for the main content
    main_container = st.container()
    
    with main_container:
        st.write("Record your voice, and analyze the emotions!")
        
        # Audio Recording within multiple columns
        col1, col2 = st.columns([1, 2])
        with col1:
            audio = mic_recorder(
                start_prompt="⏺️ Click to start recording",
                stop_prompt="⏹️ Click to stop recording",
                key="recorder"
            )
        
        with col2:
            if audio:
                try:
                    audio_bytes = audio.get('bytes')
                    if audio_bytes:
                        # Display the audio player
                        st.audio(audio_bytes, format='audio/wav')
                        
                        # Save the audio bytes directly
                        abs_audio_path = save_audio(
                            audio_bytes=audio_bytes,
                            sample_width=2, 
                            sample_rate=44100, 
                            num_channels=1
                        )
                        
                        # Store the path in session state
                        st.session_state['audio_path'] = abs_audio_path
                        st.success("Audio saved and verified successfully!")
                    
                    else:
                        st.error("No audio data received from the recorder.")
                        raise ValueError("Received empty audio bytes.")
                        
                except Exception as e:
                    st.error(f"Error saving audio: {str(e)}")
                    return
        
        # Sentiment display options with horizontal radio buttons
        display_option = st.radio(
            "Select display options for Sentiments:",
            ["Sentiment Only", "Sentiment with Points"],
            key="display_option",
            horizontal=True
        )

        # Process button
        if st.button("Get Sentiments"):
            if 'audio_path' in st.session_state:
                with st.spinner("Processing..."):
                    try:
                        # Transcribe audio
                        transcription = models.transcribe_audio(st.session_state['audio_path'])
                        
                        # Display transcription
                        st.markdown("### 📝 Transcription")
                        st.markdown(f"*{transcription}*")
                        
                        # Analyze sentiment
                        sentiment_results = models.analyze_sentiment(transcription)
                        
                        # Display results in multiple columns
                        st.markdown("### 🎭 Detected Emotions")
                        col1, col2 = st.columns(2)
                        with col1:
                            for sentiment, score in sentiment_results.items():
                                emoji = get_sentiment_emoji(sentiment)
                                if display_option == "Sentiment with Points":
                                    st.markdown(f"**{sentiment}** {emoji}: {score:.2f}")
                                else:
                                    st.markdown(f"**{sentiment}** {emoji}")
                    
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")
            else:
                st.warning("Please record audio first!")
        
        # Footer
        st.markdown('''
            ---
            Transcription by [OpenAI Whisper](https://github.com/openai/whisper) | 
            Sentiment Analysis by this [Model](https://huggingface.co/SamLowe/roberta-base-go_emotions)
        ''')

if __name__ == '__main__':
    main()































# import streamlit as st
# from src.backend.models import Models
# from src.backend.utils import save_audio, get_sentiment_emoji, verify_audio_file
# import os

# from streamlit_mic_recorder import mic_recorder

# def main():
#     # Initialize Models
#     models = Models()
    
#     # Streamlit App Structure
#     st.set_page_config(
#         page_title="🎤 Real-time Speech Emotion Recognition",
#         layout="centered",
#         initial_sidebar_state="collapsed"
#     )
#     st.title("🎤 Real-time Speech Emotion Recognition 💬")

#     # Create a container for the main content
#     main_container = st.container()
    
#     with main_container:
#         st.write("Record your voice, and analyze the emotions!")
        
#         # Audio Recording
#         audio = mic_recorder(
#             start_prompt="⏺️ Click to start recording",
#             stop_prompt="⏹️ Click to stop recording",
#             key="recorder"
#         )
        
#         if audio:
#             try:
#                 audio_bytes = audio.get('bytes')
#                 if audio_bytes:
#                     # Display the audio player
#                     st.audio(audio_bytes, format='audio/wav')
                    
#                     # # Extract audio parameters
#                     # sample_width = audio.get("sample_width", 2)
#                     # sample_rate = audio.get("sample_rate", 44100)
#                     # num_channels = audio.get("num_channels", 1)
                    
#                     # Save the audio bytes directly
#                     abs_audio_path = save_audio(
#                         audio_bytes=audio_bytes,
#                         sample_width=2, 
#                         sample_rate=44100, 
#                         num_channels=1
                        
#                         )
                    
#                     # # Verify the saved audio file
#                     # verify_audio_file(abs_audio_path)
                    
#                     # Store the path in session state
#                     st.session_state['audio_path'] = abs_audio_path
#                     st.success("Audio saved and verified successfully!")
                    
#                 else:
#                     st.error("No audio data received from the recorder.")
#                     raise ValueError("Received empty audio bytes.")
                    
#             except Exception as e:
#                 st.error(f"Error saving audio: {str(e)}")
#                 return
        
#         # Sentiment display options
#         display_option = st.radio(
#             "Select display option:",
#             ["Sentiment Only", "Sentiment + Score"],
#             key="display_option"
#         )

#         # Process button
#         if st.button("Get Sentiments"):
#             if 'audio_path' in st.session_state:
#                 with st.spinner("Processing..."):
#                     try:
#                         # Transcribe audio
#                         transcription = models.transcribe_audio(st.session_state['audio_path'])
                        
#                         # Display transcription
#                         st.markdown("### 📝 Transcription")
#                         st.markdown(f"*{transcription}*")
                        
#                         # Analyze sentiment
#                         sentiment_results = models.analyze_sentiment(transcription)
                        
#                         # Display results
#                         st.markdown("### 🎭 Detected Emotions")
#                         for sentiment, score in sentiment_results.items():
#                             emoji = get_sentiment_emoji(sentiment)
#                             if display_option == "Sentiment + Score":
#                                 st.markdown(f"**{sentiment}** {emoji}: {score:.2f}")
#                             else:
#                                 st.markdown(f"**{sentiment}** {emoji}")
                    
#                     except Exception as e:
#                         st.error(f"Error during processing: {str(e)}")
#             else:
#                 st.warning("Please record audio first!")
        
#         # Footer
#         st.markdown('''
#             ---
#             Whisper Model by [OpenAI](https://github.com/openai/whisper) | 
#             Sentiment Analysis by [SamLowe](https://huggingface.co/SamLowe/roberta-base-go_emotions)
#         ''')

# if __name__ == '__main__':
#     main()










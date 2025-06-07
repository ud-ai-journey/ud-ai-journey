# Day 53: Real-Time Language Translator with AI + Streamlit + Voice Input
# A web app that translates spoken language in real-time using Gemini API and Streamlit.

import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize Translator and Recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Streamlit page configuration
st.set_page_config(page_title="Real-Time Language Translator 🌐", page_icon="🎤", layout="centered")

# Title and description
st.title("🌐 Real-Time Language Translator")
st.markdown("Break language barriers with AI! Speak into your mic, select languages, and get instant translations. 🎙️")

# Language options (simplified list for demo)
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Telugu": "te",
}

# UI: Language selectors
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
with col2:
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1)

# Voice input button
if st.button("🎙️ Speak Now"):
    with st.spinner("Listening..."):
        try:
            # Capture audio from microphone
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)

            # Convert speech to text
            spoken_text = recognizer.recognize_google(audio, language=LANGUAGES[source_lang])
            st.session_state["spoken_text"] = spoken_text
            st.success(f"🎉 Recognized: **{spoken_text}**")
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display spoken text if available
if "spoken_text" in st.session_state and st.session_state["spoken_text"]:
    spoken_text = st.session_state["spoken_text"]

    # Translation using Gemini API
    with st.spinner("Translating with Gemini AI..."):
        try:
            # Craft the Gemini prompt for translation
            prompt = f"""
            You are a professional translator with expertise in natural and fluent translations. Translate the following text from {source_lang} to {target_lang}. Ensure the translation is natural, contextually accurate, and suitable for casual conversation.

            Text to translate: "{spoken_text}"

            Return only the translated text.
            """

            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Generate translation
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 100,
                    "temperature": 0.7,
                }
            )

            translated_text = response.text.strip()
            st.session_state["translated_text"] = translated_text

        except Exception as e:
            st.warning(f"❌ Gemini API error: {str(e)}. Falling back to googletrans.")
            # Fallback to googletrans if Gemini fails
            try:
                translation = translator.translate(spoken_text, src=LANGUAGES[source_lang], dest=LANGUAGES[target_lang])
                translated_text = translation.text
                st.session_state["translated_text"] = translated_text
            except Exception as e:
                st.error(f"❌ Translation error: {str(e)}")
                translated_text = None

    # Display translated text
    if "translated_text" in st.session_state and st.session_state["translated_text"]:
        translated_text = st.session_state["translated_text"]
        st.subheader("✨ Translated Text")
        st.markdown(f"**{source_lang} → {target_lang}:** {translated_text}")

        # Text-to-speech for translated text
        if st.button("🔊 Play Translation"):
            try:
                tts = gTTS(text=translated_text, lang=LANGUAGES[target_lang], slow=False)
                audio_file = BytesIO()
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                st.audio(audio_file, format="audio/mp3")
            except Exception as e:
                st.error(f"❌ TTS error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Built by Boya Uday Kumar** | Part of 100 Days of Python + AI Challenge | June 2025")
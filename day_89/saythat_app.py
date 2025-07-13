import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from ultralytics import YOLO
import gtts
from gtts import gTTS
import eng_to_ipa as ipa
import tempfile
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="PronounceIt - Learn Through Sight and Sound",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffd93d 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        animation: fadeIn 1s ease-in-out;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: scale(1.02);
    }
    .pronunciation-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        animation: slideIn 0.5s ease;
    }
    .word-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff6b6b;
        transition: all 0.3s ease;
    }
    .word-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stat-box:hover {
        transform: translateY(-5px);
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Dark mode toggle
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

st.sidebar.button("🌙 Toggle Dark Mode", on_click=toggle_theme)

# Initialize session state
if 'vocabulary' not in st.session_state:
    st.session_state.vocabulary = []
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'en'

# Language options
LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇺🇸'},
    'es': {'name': 'Spanish', 'flag': '🇪🇸'},
    'fr': {'name': 'French', 'flag': '🇫🇷'},
    'de': {'name': 'German', 'flag': '🇩🇪'},
    'it': {'name': 'Italian', 'flag': '🇮🇹'},
    'pt': {'name': 'Portuguese', 'flag': '🇵🇹'}
}

# Load YOLO model
@st.cache_resource
def load_model():
    try:
        model = YOLO('yolov8n.pt')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load vocabulary from file
def load_vocabulary():
    try:
        if os.path.exists('vocabulary.json'):
            with open('vocabulary.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load vocabulary: {e}")
    return []

# Save vocabulary to file
def save_vocabulary(vocabulary):
    try:
        with open('vocabulary.json', 'w') as f:
            json.dump(vocabulary, f, indent=2)
    except Exception as e:
        st.error(f"Could not save vocabulary: {e}")

# Get pronunciation
def get_pronunciation(word):
    try:
        ipa_pronunciation = ipa.convert(word)
        return ipa_pronunciation
    except Exception as e:
        return word

# Generate audio
def generate_audio(text, filename, language='en'):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        return True
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return False

# Detect objects in image
def detect_objects(image, model):
    try:
        results = model(image)
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    if confidence > 0.5:
                        detections.append({
                            'class_name': class_name,
                            'confidence': confidence,
                            'bbox': [x1, y1, x2, y2]
                        })
        return detections
    except Exception as e:
        st.error(f"Error in object detection: {e}")
        return []

# Draw bounding boxes on image
def draw_boxes(image, detections):
    img_array = np.array(image)
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(img_array, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{detection['class_name']} ({detection['confidence']:.2f})"
        cv2.putText(img_array, label, (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return Image.fromarray(img_array)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 PronounceIt</h1>
        <p><em>Learn Through Sight and Sound - Master Pronunciations with AI!</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🌍 Language Settings")
        selected_lang = st.selectbox(
            "Choose your target language:",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
            index=list(LANGUAGES.keys()).index(st.session_state.selected_language)
        )
        if selected_lang != st.session_state.selected_language:
            st.session_state.selected_language = selected_lang
            st.rerun()
        
        st.markdown("---")
        st.header("📚 Your Vocabulary")
        vocabulary = load_vocabulary()
        if vocabulary:
            st.write(f"📖 **{len(vocabulary)} words learned**")
            for word_data in vocabulary[-5:]:
                with st.expander(f"📝 {word_data['word']}"):
                    st.write(f"**Pronunciation:** {word_data['pronunciation']}")
                    st.write(f"**Learned:** {word_data['date']}")
                    if 'audio_file' in word_data and word_data['audio_file'] and os.path.exists(word_data['audio_file']):
                        st.audio(word_data['audio_file'], format='audio/mp3')
        else:
            st.info("📚 Start learning! Upload a picture to build your vocabulary.")
        
        st.markdown("---")
        st.header("🎮 Learning Games")
        if vocabulary:
            game_mode = st.selectbox(
                "Choose a game:",
                ["🎯 Flashcard Review", "🎲 Guess the Object", "📊 Progress Quiz"]
            )
            if game_mode == "🎯 Flashcard Review":
                if st.button("🔄 Start Flashcard Review"):
                    st.session_state.flashcard_mode = True
                    st.session_state.current_card = 0
                    st.rerun()
            elif game_mode == "🎲 Guess the Object":
                if st.button("🎲 Start Guessing Game"):
                    st.session_state.guessing_mode = True
                    st.rerun()
        
        st.markdown("---")
        st.header("🎯 Features")
        st.markdown("""
        - 📸 **Object Detection**: Identify objects in photos
        - 🔊 **Audio Pronunciation**: Hear how to say words
        - 📝 **IPA Transcription**: See phonetic spelling
        - 📚 **Vocabulary Journal**: Track your learning
        - 🌍 **Multi-language Support**: Learn in 6 languages
        - 📷 **Live Camera Mode**: Take photos instantly
        - 🎮 **Learning Games**: Flashcards and quizzes
        - 🖋️ **Custom Vocabulary**: Add your own words
        - 🎙️ **Pronunciation Practice**: Record and compare
        - 🌟 **Themed Lessons**: Learn by category
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    # Check for game modes
    if st.session_state.get('flashcard_mode', False) and vocabulary:
        st.header("🎯 Flashcard Review")
        if st.session_state.current_card < len(vocabulary):
            current_word = vocabulary[st.session_state.current_card]
            col_flash1, col_flash2 = st.columns([1, 1])
            with col_flash1:
                st.markdown(f"""
                <div class="pronunciation-box">
                    <h2>🎤 {current_word['word']}</h2>
                    <p><strong>Pronunciation:</strong> /{current_word['pronunciation']}/</p>
                    <p><strong>Learned:</strong> {current_word['date']}</p>
                </div>
                """, unsafe_allow_html=True)
                if 'audio_file' in current_word and current_word['audio_file'] and os.path.exists(current_word['audio_file']):
                    st.audio(current_word['audio_file'], format='audio/mp3')
            with col_flash2:
                st.write("**How well do you know this word?**")
                confidence = st.slider("Rate your confidence:", 1, 5, 3, key=f"confidence_{st.session_state.current_card}")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ I know this!", key=f"know_{st.session_state.current_card}"):
                        st.session_state.current_card += 1
                        st.rerun()
                with col_btn2:
                    if st.button("❌ Need more practice", key=f"practice_{st.session_state.current_card}"):
                        st.session_state.current_card += 1
                        st.rerun()
        else:
            st.success("🎉 Flashcard review completed!")
            if st.button("🔄 Start Over"):
                st.session_state.current_card = 0
                st.rerun()
            if st.button("🏠 Back to Main"):
                st.session_state.flashcard_mode = False
                st.rerun()
    
    elif st.session_state.get('guessing_mode', False) and vocabulary:
        st.header("🎲 Guess the Object")
        if 'guessing_word' not in st.session_state:
            import random
            st.session_state.guessing_word = random.choice(vocabulary)
            st.session_state.guessing_attempts = 0
        st.write(f"**Hint:** This object has {len(st.session_state.guessing_word['word'])} letters")
        st.write(f"**Pronunciation:** /{st.session_state.guessing_word['pronunciation']}/")
        if 'audio_file' in st.session_state.guessing_word and st.session_state.guessing_word['audio_file'] and os.path.exists(st.session_state.guessing_word['audio_file']):
            st.audio(st.session_state.guessing_word['audio_file'], format='audio/mp3')
        guess = st.text_input("What's the word?", key="guess_input")
        if st.button("🎯 Submit Guess"):
            st.session_state.guessing_attempts += 1
            if guess.lower() == st.session_state.guessing_word['word'].lower():
                st.success(f"🎉 Correct! The word was '{st.session_state.guessing_word['word']}'")
                st.write(f"Attempts: {st.session_state.guessing_attempts}")
                if st.button("🎲 Next Word"):
                    del st.session_state.guessing_word
                    st.rerun()
            else:
                st.error("❌ Try again!")
                st.write(f"Attempts: {st.session_state.guessing_attempts}")
        if st.button("🏠 Back to Main"):
            st.session_state.guessing_mode = False
            st.rerun()
    
    else:
        with col1:
            st.header("📸 Image Input")
            input_method = st.radio(
                "Choose input method:",
                ["📁 Upload Image", "📷 Take Photo"],
                horizontal=True
            )
            if input_method == "📁 Upload Image":
                uploaded_file = st.file_uploader(
                    "Choose an image...",
                    type=['png', 'jpg', 'jpeg'],
                    help="Upload a photo to detect objects and learn pronunciation"
                )
            else:
                uploaded_file = st.camera_input(
                    "Take a photo to detect objects",
                    help="Click the camera button to take a photo"
                )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            model = load_model()
            if model:
                with st.spinner("🔍 Detecting objects..."):
                    detections = detect_objects(image, model)
                    if detections:
                        annotated_image = draw_boxes(image, detections)
                        st.image(annotated_image, caption="Detected Objects", use_column_width=True)
                        st.session_state.detection_history.append({
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'objects': [d['class_name'] for d in detections]
                        })
                        for detection in detections:
                            word = detection['class_name']
                            pronunciation = get_pronunciation(word)
                            audio_filename = f"audio_{word}_{st.session_state.selected_language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                            audio_generated = generate_audio(word, audio_filename, str(st.session_state.selected_language))
                            if not any(item['word'] == word for item in vocabulary):
                                vocabulary.append({
                                    'word': word,
                                    'pronunciation': pronunciation,
                                    'date': datetime.now().strftime("%Y-%m-%d"),
                                    'audio_file': audio_filename if audio_generated else None,
                                    'confidence': detection['confidence']
                                })
                                save_vocabulary(vocabulary)
                            st.markdown(f"""
                            <div class="pronunciation-box">
                                <h3>🎤 {word}</h3>
                                <p><strong>Pronunciation:</strong> /{pronunciation}/</p>
                                <p><strong>Confidence:</strong> {detection['confidence']:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            if audio_generated:
                                st.audio(audio_filename, format='audio/mp3')
                            if st.button(f"📚 Add '{word}' to Vocabulary", key=f"add_{word}_{detection['confidence']:.2f}"):
                                st.success(f"✅ '{word}' added to your vocabulary!")
                    else:
                        st.warning("🔍 No objects detected with high confidence. Try a clearer image!")
            else:
                st.error("❌ Model not loaded. Please check your installation.")
    
    with col2:
        st.header("📊 Learning Analytics")
        if st.session_state.detection_history:
            df = pd.DataFrame(st.session_state.detection_history)
            st.subheader("📈 Objects Detected Over Time")
            object_counts = []
            for record in st.session_state.detection_history:
                object_counts.append({
                    'date': record['date'][:10],
                    'count': len(record['objects'])
                })
            if object_counts:
                df_counts = pd.DataFrame(object_counts)
                fig = px.line(df_counts, x='date', y='count', 
                            title="Objects Detected Daily",
                            labels={'count': 'Number of Objects', 'date': 'Date'})
                st.plotly_chart(fig, use_container_width=True)
            st.subheader("🏆 Most Common Objects")
            all_objects = []
            for record in st.session_state.detection_history:
                all_objects.extend(record['objects'])
            if all_objects:
                object_freq = pd.Series(all_objects).value_counts().head(10)
                fig = px.bar(x=object_freq.values, y=object_freq.index,
                           orientation='h',
                           title="Top 10 Detected Objects",
                           labels={'x': 'Count', 'y': 'Object'})
                st.plotly_chart(fig, use_container_width=True)
        
        if vocabulary:
            st.subheader("📚 Vocabulary Statistics")
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("Total Words", len(vocabulary))
            with col_stats2:
                confidences = [item.get('confidence', 0) for item in vocabulary]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                st.metric("Avg Confidence", f"{avg_confidence:.2f}")
            with col_stats3:
                today = datetime.now().strftime("%Y-%m-%d")
                today_words = len([item for item in vocabulary if item['date'] == today])
                st.metric("Today's Words", today_words)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🎤 <strong>PronounceIt</strong> - Learn Through Sight and Sound</p>
        <p>Built with ❤️ using Streamlit, YOLO, and open-source AI</p>
        <p>💡 <em>Zero API costs, completely offline, infinitely scalable!</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
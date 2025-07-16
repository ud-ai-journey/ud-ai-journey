import streamlit as st
import os
import json
from datetime import datetime

DATA_FILE = os.path.join("data", "kid_diary_entries.json")

def save_entry(entry):
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            entries = json.load(f)
    else:
        entries = []
    entries.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

st.set_page_config(page_title="KidDiary.ai – Magical Journaling for Kids", page_icon="🧒")

st.title("🌟 KidDiary.ai – Magical Journaling for Kids")
st.write("A magical daily journal for kids to express their feelings and get kind feedback from Doodle the Diary Dragon!")

# Add imports for emotion classifier, story generator, and companion reply
from models.emotion_classifier import classify_emotion
from utils.diary_story import generate_story
from utils.companion_reply import doodle_reply

# Input section
st.header("How was your day, buddy?")
input_mode = st.radio("Choose input mode:", ("Text", "Voice (coming soon)"))

if input_mode == "Text":
    kid_input = st.text_area("Type your thoughts here:", "I played with my puppy and it was fun!")
    submit = st.button("Submit")
else:
    st.info("Voice input will be available soon!")
    kid_input = ""
    submit = False

# Placeholder for emotion detection and story generation
if submit and kid_input.strip():
    emotion, color, emoji = classify_emotion(kid_input)
    st.subheader("🔍 Detecting emotion...")
    st.write(f"Emotion: {emotion}")
    st.write(f"Color: {color} {emoji}")
    story = generate_story(kid_input, emotion)
    st.subheader("📝 Your Magical Diary Story")
    st.write(story)
    st.subheader("🧙‍♂️ Doodle the Diary Dragon says:")
    st.success(doodle_reply(emotion))
    st.balloons()
    # Save entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": kid_input,
        "emotion": emotion,
        "color": color,
        "emoji": emoji,
        "story": story
    }
    save_entry(entry)

# Timeline view
st.header("📅 Your Diary Timeline")
entries = load_entries()
if entries:
    for e in reversed(entries[-10:]):
        st.write(f"{e['timestamp'][:10]} {e['emoji']} {e['story']}")
else:
    st.info("No diary entries yet. Start your magical journey!") 
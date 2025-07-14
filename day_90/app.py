import streamlit as st
import json
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Load art style mappings ---
with open('art_styles.json', 'r') as f:
    ART_STYLES = json.load(f)

# --- App Title ---
st.set_page_config(page_title="EmotiGram – AI Mood-to-Art Generator", layout="centered")
st.title("🎨 EmotiGram – AI Mood-to-Art Generator")
st.write("Upload a selfie or record your voice, and get a beautiful artwork that matches your mood!")

# --- Sidebar: Input Method ---
st.sidebar.header("Input Method")
input_method = st.sidebar.radio("Choose input method:", ["Selfie (Image)", "Voice (Audio)"])

# --- Sidebar: User Name ---
user_name = st.sidebar.text_input("Your Name (optional)", "")

# --- Main: Upload or Record ---
emotion = None
uploaded_image = None
uploaded_audio = None

if input_method == "Selfie (Image)":
    uploaded_image = st.file_uploader("Upload a selfie/photo", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        st.image(image, caption="Your uploaded image", use_column_width=True)
        # --- Emoji-fy Button ---
        if st.button("Emoji-fy Me!"):
            import cv2
            import numpy as np
            # Convert PIL to OpenCV
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # --- (1) Face detection (optional, fallback to whole image) ---
            face_cascade = cv2.CascadeClassifier(str(cv2.data.haarcascades) + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                face_img = img_cv[y:y+h, x:x+w]
            else:
                face_img = img_cv
            # Resize to square
            face_img = cv2.resize(face_img, (256, 256))
            # --- (2) Cartoon effect ---
            # Edge mask
            gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            gray_face = cv2.medianBlur(gray_face, 7)
            edges = cv2.adaptiveThreshold(gray_face, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
            # Color quantization
            data_kmeans = np.float32(face_img).reshape((-1, 3))
            K = 8
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
            dummy_labels = np.zeros((data_kmeans.shape[0], 1), dtype=np.int32)
            _, label, center = cv2.kmeans(data_kmeans, K, dummy_labels, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            label = np.array(label).flatten().astype(np.int32)
            center = np.array(center)
            result = center[label].reshape(face_img.shape)
            # Combine edges and quantized color
            cartoon = cv2.bitwise_and(result, result, mask=edges)
            # --- (3) Crop to circle ---
            mask = np.zeros((256, 256), np.uint8)
            cv2.circle(mask, (128, 128), 120, (255,), -1)
            cartoon_circle = cv2.bitwise_and(cartoon, cartoon, mask=mask)
            # --- (4) Add yellow background (emoji style) ---
            bg = np.ones((256, 256, 3), np.uint8) * np.array([255, 221, 51], np.uint8)  # emoji yellow
            inv_mask = cv2.bitwise_not(mask)
            bg_masked = cv2.bitwise_and(bg, bg, mask=inv_mask)
            emoji_img = cv2.add(bg_masked, cartoon_circle)
            # Convert back to PIL
            emoji_pil = Image.fromarray(cv2.cvtColor(emoji_img, cv2.COLOR_BGR2RGB))
            st.image(emoji_pil, caption="Your Emoji-fied Selfie!", use_column_width=False)
            # --- (5) Download button ---
            from io import BytesIO
            buf = BytesIO()
            emoji_pil.save(buf, format='PNG')
            st.download_button("Download Emoji", buf.getvalue(), file_name="emoji_selfie.png", mime="image/png")
        # --- Placeholder: Detect emotion from image ---
        st.info("[Placeholder] Detecting emotion from face...")
        # TODO: Integrate FER or other emotion detection here
        emotion = st.selectbox("Detected Emotion (demo)", list(ART_STYLES.keys()), index=0)

elif input_method == "Voice (Audio)":
    uploaded_audio = st.file_uploader("Upload a short audio clip (WAV/MP3)", type=["wav", "mp3"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        # --- Placeholder: Detect emotion from audio ---
        st.info("[Placeholder] Detecting emotion from voice...")
        # TODO: Integrate Whisper + sentiment analysis here
        emotion = st.selectbox("Detected Emotion (demo)", list(ART_STYLES.keys()), index=0)

# --- Map emotion to art style ---
if emotion:
    st.subheader(f"Detected Emotion: :rainbow[{emotion.capitalize()}]")
    art_prompt = ART_STYLES.get(emotion, "A beautiful digital painting")
    st.write(f"**Art Style Prompt:** {art_prompt}")

    # --- Generate AI Art Button ---
    if st.button("✨ Generate AI Art!"):
        with st.spinner("Generating your mood art with AI... this may take a moment!"):
            from diffusers import StableDiffusionPipeline
            import torch
            # Load pipeline (cache for session)
            if 'sd_pipe' not in st.session_state:
                st.session_state['sd_pipe'] = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                if torch.cuda.is_available():
                    st.session_state['sd_pipe'] = st.session_state['sd_pipe'].to("cuda")
            pipe = st.session_state['sd_pipe']
            # Generate image
            image_out = pipe(art_prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
            st.image(image_out, caption="Your AI-Generated Mood Art!", use_column_width=True)
            # Download button
            from io import BytesIO
            buf = BytesIO()
            image_out.save(buf, format='PNG')
            st.download_button("Download AI Art", buf.getvalue(), file_name=f"ai_art_{emotion}.png", mime="image/png")

    # --- Placeholder: Generate image (replace with Stable Diffusion later) ---
    # For now, create a simple colored image with the emotion as text
    img = Image.new('RGB', (512, 512), color=(240, 240, 255))
    draw = ImageDraw.Draw(img)
    font_size = 40
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    text = f"{emotion.capitalize()}"
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((512-w)/2, (512-h)/2), text, fill=(80, 80, 200), font=font)
    # Add user name as sticker/caption if provided
    if user_name.strip():
        caption = f"{user_name}"
        draw.rectangle([(0, 470), (512, 512)], fill=(255,255,255,200))
        draw.text((10, 475), caption, fill=(0,0,0), font=font)
    st.image(img, caption="[Placeholder] Generated Mood Artwork", use_column_width=True)

    # --- Download button ---
    img_bytes = None
    from io import BytesIO
    buf = BytesIO()
    img.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    st.download_button("Download Your EmotiGram", img_bytes, file_name=f"emotigram_{emotion}.png", mime="image/png")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ for Day 90 of the 100 Days Python & AI Challenge") 
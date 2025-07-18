import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from image_analyzer import detect_objects
from story_generator import generate_cohesive_story, generate_title, generate_social_captions
from tts import text_to_speech
from streamlit_sortables import sort_items
from streamlit_cropper import st_cropper
import tempfile
import io
import os
import numpy as np
from fpdf import FPDF

# --- Adaptive Theme Colors ---
LIGHT_BG = "#F7F8FA"
DARK_BG = "#181A1B"
ACCENT = "#6C63FF"
SUCCESS = "#00C896"
ERROR = "#FF6B6B"

st.set_page_config(
    page_title="Memory Lane: Picture to Story",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Custom CSS for Adaptive Theme ---
st.markdown(f"""
    <style>
    html, body, .stApp {{
        background: {LIGHT_BG};
        color: #22223B;
        font-family: 'Inter', 'Nunito', 'Roboto', Arial, sans-serif;
    }}
    @media (prefers-color-scheme: dark) {{
        html, body, .stApp {{
            background: {DARK_BG} !important;
            color: #F7F8FA !important;
        }}
        .stButton>button {{ background: {ACCENT} !important; color: #fff !important; }}
    }}
    .stButton>button {{
        background: {ACCENT};
        color: #fff;
        border-radius: 8px;
        padding: 0.75em 2em;
        font-size: 1.1em;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 8px 0 rgba(108,99,255,0.10);
        transition: background 0.2s;
    }}
    .stButton>button:hover {{
        background: #5548c8;
    }}
    .stTextInput>div>input, .stTextArea>div>textarea {{
        border-radius: 8px;
        font-size: 1.05em;
    }}
    .stFileUploader>div {{
        border-radius: 8px;
    }}
    .stAlert, .stInfo {{
        border-radius: 8px;
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {ACCENT} !important;
        font-weight: 700;
    }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Nunito:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🖼️ Memory Lane: Picture to Story</h1>", unsafe_allow_html=True)
st.caption("Turn your photos into narrated stories with AI. Beautiful, emotional, and mobile-friendly.")

# --- Multi-image upload and memory input ---
uploaded_files = st.file_uploader(
    "Upload up to 5 images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="multi_image_uploader"
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("Please upload no more than 5 images.")
        uploaded_files = uploaded_files[:5]
    # Prepare image-memory pairs
    image_memory_pairs = []
    for idx, file in enumerate(uploaded_files):
        image = Image.open(file)
        # Cropper
        st.write(f"#### ✂️ Crop and Filter Image {idx+1}")
        crop_result = st_cropper(image, box_color=ACCENT, aspect_ratio=(1, 1), return_type='image', key=f'cropper_{idx}')  # type: ignore
        if isinstance(crop_result, Image.Image):
            cropped_img = crop_result
        elif isinstance(crop_result, (tuple, list)):
            cropped_img = crop_result[0]
        elif isinstance(crop_result, dict) and 'image' in crop_result:
            cropped_img = crop_result['image']
        else:
            cropped_img = image
        filter_option = st.selectbox(
            f"Apply a filter to Image {idx+1}",
            ["None", "Grayscale", "Sepia", "Blur"],
            key=f"filter_{idx}"
        )
        if filter_option == "Grayscale":
            cropped_img = ImageOps.grayscale(cropped_img).convert("RGB")
        elif filter_option == "Sepia":
            sepia = ImageOps.colorize(ImageOps.grayscale(cropped_img), '#704214', '#C0C080')
            cropped_img = sepia.convert("RGB")
        elif filter_option == "Blur":
            cropped_img = cropped_img.filter(ImageFilter.GaussianBlur(radius=3))
        st.image(cropped_img, caption=f"Preview Image {idx+1}", use_container_width=True)
        memory = st.text_area(f"What do you remember or feel about Image {idx+1}?", key=f"memory_{idx}")
        image_memory_pairs.append({"image": cropped_img, "memory": memory, "idx": idx})
    # Drag-and-drop ordering
    st.markdown("#### 🟰 Drag to reorder your images:")
    image_labels = [f"Image {i['idx']+1}" for i in image_memory_pairs]
    ordered_labels = sort_items(image_labels, direction="horizontal")
    ordered_pairs = [image_memory_pairs[image_labels.index(label)] for label in ordered_labels]
    images = [pair["image"] for pair in ordered_pairs]
    memories = [pair["memory"] for pair in ordered_pairs]
    st.session_state["images"] = images
    st.session_state["memories"] = memories
    # Collage template selector
    collage_template = st.selectbox("Choose your collage style:", ["Grid", "Polaroid", "Overlapping"], key="collage_template")
    # Story tone selector
    story_tone = st.selectbox("Choose your story tone:", ["Nostalgic", "Funny", "Poetic", "Dramatic", "Heartwarming"], key="story_tone")
    if all(memories) and st.button("Generate My Memory Lane Story", use_container_width=True):
        with st.spinner("Weaving your memories into a beautiful story..."):
            story = generate_cohesive_story(memories, tone=story_tone)
        with st.spinner("Creating the perfect title..."):
            title = generate_title(memories)
        # Save story and collage in session state history
        if "history" not in st.session_state:
            st.session_state["history"] = []
        # Save current collage as PNG bytes
        def create_collage(images, template="Grid", collage_width=800, collage_height=400, padding=10):
            n = len(images)
            if n == 0:
                return None
            if template == "Grid":
                grid_cols = min(n, 3)
                grid_rows = (n + 2) // 3
                thumb_w = (collage_width - (grid_cols + 1) * padding) // grid_cols
                thumb_h = (collage_height - (grid_rows + 1) * padding) // grid_rows
                collage = Image.new('RGB', (collage_width, collage_height), color=(255,255,255))
                for idx, img in enumerate(images):
                    row = idx // 3
                    col = idx % 3
                    thumb = img.copy().resize((thumb_w, thumb_h))
                    x = padding + col * (thumb_w + padding)
                    y = padding + row * (thumb_h + padding)
                    collage.paste(thumb, (x, y))
                return collage
            elif template == "Polaroid":
                import random
                collage = Image.new('RGB', (collage_width, collage_height), color=(245,245,245))
                center_x, center_y = collage_width // 2, collage_height // 2
                polaroid_w, polaroid_h = 220, 260
                offsets = [(-180, -60), (0, -80), (180, -60), (-90, 80), (90, 80)]
                for idx, img in enumerate(images):
                    thumb = img.copy().resize((180, 180))
                    polaroid = Image.new('RGB', (polaroid_w, polaroid_h), color=(255,255,255))
                    polaroid.paste(thumb, (20, 20))
                    shadow = Image.new('RGBA', (polaroid_w+8, polaroid_h+8), (0,0,0,0))
                    shadow.paste(polaroid, (4,4))
                    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
                    angle = random.randint(-15, 15)
                    polaroid = polaroid.rotate(angle, expand=1, fillcolor=(255,255,255))
                    shadow = shadow.rotate(angle, expand=1, fillcolor=(0,0,0,0))
                    dx, dy = offsets[idx % len(offsets)]
                    px = center_x + dx - polaroid.width//2
                    py = center_y + dy - polaroid.height//2
                    collage.paste(Image.alpha_composite(shadow.convert('RGBA'), polaroid.convert('RGBA')).convert('RGB'), (px, py), polaroid.convert('RGBA'))
                return collage
            elif template == "Overlapping":
                import random
                collage = Image.new('RGBA', (collage_width, collage_height), color=(255,255,255,255))
                center_x, center_y = collage_width // 2, collage_height // 2
                base_w, base_h = 200, 200
                offsets = [(-100, -40), (0, -60), (100, -40), (-50, 60), (50, 60)]
                for idx, img in enumerate(images):
                    thumb = img.copy().resize((base_w, base_h))
                    angle = random.randint(-25, 25)
                    thumb = thumb.rotate(angle, expand=1, fillcolor=(255,255,255))
                    dx, dy = offsets[idx % len(offsets)]
                    px = center_x + dx - thumb.width//2
                    py = center_y + dy - thumb.height//2
                    collage.alpha_composite(thumb.convert('RGBA'), (px, py))
                return collage.convert('RGB')
            else:
                return None
        collage = create_collage(images, template=collage_template)
        collage_bytes = None
        if collage:
            buf = io.BytesIO()
            collage.save(buf, format="PNG")
            collage_bytes = buf.getvalue()
        st.session_state["history"].append({
            "title": title,
            "story": story,
            "memories": memories,
            "collage_bytes": collage_bytes,
            "captions": None,  # will be set below
        })
        st.success(f"**{title}**")
        # Collage
        if collage:
            st.image(collage, caption="Your Memory Collage", use_container_width=True)
            buf = io.BytesIO()
            collage.save(buf, format="PNG")
            st.download_button(
                label="Download Collage as PNG",
                data=buf.getvalue(),
                file_name="memory_lane_collage.png",
                mime="image/png",
                use_container_width=True
            )
        # Animated GIF Carousel
        if len(images) > 1:
            gif_buf = io.BytesIO()
            gif_images = [img.convert("RGB").resize(images[0].size) for img in images]
            gif_images[0].save(
                gif_buf,
                format="GIF",
                save_all=True,
                append_images=gif_images[1:],
                duration=1200,
                loop=0
            )
            st.image(gif_buf.getvalue(), caption="Animated Memory Carousel", use_container_width=True)
            st.download_button(
                label="Download Animated Carousel (GIF)",
                data=gif_buf.getvalue(),
                file_name="memory_lane_carousel.gif",
                mime="image/gif",
                use_container_width=True
            )
        st.image(images, caption=[f"Image {i+1}" for i in range(len(images))], use_container_width=True)
        st.subheader("Your Memory Lane Story")
        highlighted_story = story
        for mem in memories:
            if mem.strip():
                mem_escaped = mem.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
                highlighted_story = highlighted_story.replace(mem_escaped, f"**{mem_escaped}**")
        st.markdown(highlighted_story)
        st.session_state["story"] = story
        with st.spinner("Crafting social captions..."):
            captions = generate_social_captions(memories, story, title)
        st.session_state["history"][-1]["captions"] = captions
        # PDF export
        def create_pdf(collage_bytes, title, story, captions):
            pdf = FPDF()
            pdf.add_page()
            y = 10
            if collage_bytes:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
                    tmp_img.write(collage_bytes)
                    tmp_img.flush()
                    pdf.image(tmp_img.name, x=10, y=y, w=pdf.w-20)
                    y += 80
                os.remove(tmp_img.name)
            pdf.set_xy(10, y+10)
            pdf.set_font("Arial", "B", 16)
            pdf.multi_cell(0, 10, title)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, story)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Social Captions:", ln=1)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, f"Instagram: {captions.get('instagram', '')}\nLinkedIn: {captions.get('linkedin', '')}\nX: {captions.get('x', '')}")
            pdf_str = pdf.output(dest='S')
            if isinstance(pdf_str, str):
                pdf_bytes = pdf_str.encode('latin1')
            else:
                pdf_bytes = bytes(pdf_str)
            return pdf_bytes
        pdf_bytes = create_pdf(collage_bytes, title, story, captions)
        st.download_button(
            label="Download Story as PDF",
            data=pdf_bytes,
            file_name="memory_lane_story.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        # Audio narration download
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio:
            text_to_speech(st.session_state["story"], tmp_audio.name)
            tmp_audio.seek(0)
            audio_bytes = tmp_audio.read()
        st.audio(tmp_audio.name, format="audio/mp3", start_time=0)
        st.download_button(
            label="Download Narration as MP3",
            data=audio_bytes,
            file_name="memory_lane_narration.mp3",
            mime="audio/mp3",
            use_container_width=True
        )
        os.remove(tmp_audio.name)
else:
    st.info("Upload up to 5 images to get started.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.95em;color:#888;'>Made with ❤️ | Inspired by Dribbble, Material Design, Apple HIG</div>",
    unsafe_allow_html=True
)

# Show past stories
if "history" in st.session_state and st.session_state["history"]:
    st.markdown("---")
    st.markdown("### 📚 Past Memory Lane Stories")
    for idx, entry in enumerate(reversed(st.session_state["history"])):
        st.markdown(f"**{entry['title']}**")
        if entry["collage_bytes"]:
            st.image(entry["collage_bytes"], caption="Collage", use_container_width=True)
        st.markdown(entry["story"])
        if entry["captions"]:
            st.markdown(f"**Instagram:** {entry['captions'].get('instagram', '')}")
            st.markdown(f"**LinkedIn:** {entry['captions'].get('linkedin', '')}")
            st.markdown(f"**X:** {entry['captions'].get('x', '')}")
        st.markdown("---") 
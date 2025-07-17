import streamlit as st
import plotly.express as px
from datetime import datetime
import json
import pandas as pd
import re
from utils import extract_json

from ai_helper import AIHelper
from vault_manager import VaultManager
from spaced_repetition import SpacedRepetition

# Initialize components
ai_model = "llama3-8b-8192"  # Default model
ai_helper = AIHelper(model=ai_model)
vault_manager = VaultManager()
spaced_repetition = SpacedRepetition()

# Set page config
st.set_page_config(
    page_title="MemoryVault.ai",
    page_icon="🧠",
    layout="wide"
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Add Entry", "Review Flashcards", "Random Review", "Dashboard"]
)

# Add Entry Page
if page == "Add Entry":
    st.title("🧠 Add Learning Entry")
    
    with st.form("entry_form"):
        title = st.text_input("Title", placeholder="e.g., Python Decorators", help="What did you learn? Give it a short, clear title.")
        notes = st.text_area("Notes/Highlights", placeholder="Enter your learning notes here...", help="Summarize what you learned, key points, or highlights.")
        tag = st.selectbox("Tag", ["AI", "Personal Growth", "Coding", "Other"], help="Categorize your learning for easy filtering.")
        mood = st.slider("Learning Mood", 1, 5, 3, help="How do you feel about this learning? (1: Confused, 5: Confident)")
        
        submit = st.form_submit_button("Save Entry")
        
        if submit and title and notes:
            with st.spinner("Generating AI summary and flashcards..."):
                # Generate AI summary
                summary = ai_helper.generate_summary(title, notes, tag)
                
                # Generate flashcards
                flashcards_json = ai_helper.generate_flashcards(title, notes, tag)
                flashcards = extract_json(flashcards_json)
                if not flashcards:
                    st.error("Error parsing AI-generated flashcards. Using empty set.")
                    with st.expander("Show raw AI output"):
                        st.write(flashcards_json)
                
                # Calculate next review date
                next_review = spaced_repetition.get_initial_review_date()
                
                # Save entry
                entry_id = vault_manager.add_entry(
                    title=title,
                    notes=notes,
                    tag=tag,
                    mood=mood,
                    summary=summary,
                    flashcards=flashcards,
                    next_review=next_review
                )
                
                st.success("Entry saved successfully! 🎉")
                st.subheader("AI Summary")
                st.write(summary)
                
                st.subheader("Generated Flashcards")
                for card in flashcards:
                    with st.expander(f"Q: {card['question']}"):
                        st.write(f"A: {card['answer']}")

# Review Flashcards Page
elif page == "Review Flashcards":
    st.title("🎯 Review Flashcards")
    
    due_cards = vault_manager.get_due_flashcards()
    
    if not due_cards:
        st.info("No flashcards due for review! 🎉")
    else:
        st.write(f"{len(due_cards)} cards due for review")
        
        for card in due_cards:
            with st.expander(f"Review: {card['question']}"):
                st.write("Answer:", card['answer'])
                quality = st.slider(
                    "How well did you know this?",
                    0, 5, 3,
                    key=f"slider_{card.get('id', id(card))}",
                    help="0: Complete blackout, 5: Perfect recall"
                )
                if st.button(f"Record Review for card {card.get('id', 'unknown')}"):
                    vault_manager.record_review(card.get('id'), quality, spaced_repetition=spaced_repetition)
                    st.success("Review recorded!")

# Random Review Page
elif page == "Random Review":
    st.title("🎲 Random Review Mode")
    import random
    all_cards = vault_manager.flashcards
    if not all_cards:
        st.info("No flashcards available for review!")
    else:
        card = random.choice(all_cards)
        st.write(f"**Q:** {card['question']}")
        if st.button("Show Answer"):
            st.write(f"**A:** {card['answer']}")
        quality = st.slider(
            "How well did you know this?",
            0, 5, 3,
            key=f"random_slider_{card.get('id', id(card))}",
            help="0: Complete blackout, 5: Perfect recall"
        )
        if st.button(f"Record Review for card {card.get('id', 'unknown')}"):
            vault_manager.record_review(card.get('id'), quality, spaced_repetition=spaced_repetition)
            st.success("Review recorded!")

# Dashboard Page
else:
    st.title("📊 Learning Dashboard")
    stats = vault_manager.get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Entries", stats["total_entries"])
    with col2:
        st.metric("Total Flashcards", stats["total_cards"])
    with col3:
        st.metric("Total Reviews", stats["total_reviews"])
    with col4:
        st.metric("Weekly Completion", f"{stats['weekly_completion']:.1f}%")
    st.subheader("Export/Backup Your Data")
    col_md, col_pdf, col_csv, col_fcsv, col_zip, col_restore = st.columns(6)
    with col_md:
        if st.button("Export to Markdown"):
            md_path = "memoryvault_export.md"
            vault_manager.export_entries_to_markdown(md_path)
            with open(md_path, "r", encoding="utf-8") as f:
                st.download_button("Download Markdown", f, file_name=md_path)
    with col_pdf:
        if st.button("Export to PDF"):
            pdf_path = "memoryvault_export.pdf"
            vault_manager.export_entries_to_pdf(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=pdf_path)
    with col_csv:
        if st.button("Export Entries CSV"):
            csv_path = "memoryvault_entries.csv"
            vault_manager.export_entries_to_csv(csv_path)
            with open(csv_path, "r", encoding="utf-8") as f:
                st.download_button("Download Entries CSV", f, file_name=csv_path)
    with col_fcsv:
        if st.button("Export Flashcards CSV"):
            fcsv_path = "memoryvault_flashcards.csv"
            vault_manager.export_flashcards_to_csv(fcsv_path)
            with open(fcsv_path, "r", encoding="utf-8") as f:
                st.download_button("Download Flashcards CSV", f, file_name=fcsv_path)
    with col_zip:
        if st.button("Backup All Data (zip)"):
            zip_path = "memoryvault_backup.zip"
            vault_manager.backup_all_data(zip_path)
            with open(zip_path, "rb") as f:
                st.download_button("Download Backup Zip", f, file_name=zip_path)
    with col_restore:
        uploaded = st.file_uploader("Restore from Backup", type="zip")
        if uploaded and st.button("Restore Now"):
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                tmp.write(uploaded.read())
                tmp.flush()
                vault_manager.restore_from_backup(tmp.name)
            st.success("Backup restored! Please refresh the app.")
    
    # Get all entries for visualization
    entries = vault_manager.get_entries()
    if entries:
        df = pd.DataFrame(entries)
        df['created_at'] = pd.to_datetime(df['created_at'])
        st.subheader("Entries by Tag")
        fig = px.pie(df, names='tag', title='Distribution of Learning Topics')
        st.plotly_chart(fig)
        st.subheader("Learning Mood Over Time")
        fig = px.line(df, x='created_at', y='mood', title='Learning Confidence Trend')
        st.plotly_chart(fig)
        st.subheader("Recent Entries (Edit/Delete)")
        recent_entries = df.sort_values('created_at', ascending=False).head()
        for _, entry in recent_entries.iterrows():
            with st.expander(f"{entry['title']} ({entry['tag']})"):
                st.write("Summary:", entry['summary'])
                st.write("Next review:", entry['next_review'])
                # Edit form
                with st.form(f"edit_entry_{entry['id']}"):
                    new_title = st.text_input("Edit Title", value=entry['title'])
                    new_notes = st.text_area("Edit Notes", value=entry['notes'])
                    new_tag = st.text_input("Edit Tag", value=entry['tag'])
                    new_mood = st.slider("Edit Mood", 1, 5, int(entry['mood']))
                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        vault_manager.edit_entry(entry['id'], title=new_title, notes=new_notes, tag=new_tag, mood=new_mood)
                        st.success("Entry updated! Please refresh to see changes.")
                # Delete button
                if st.button(f"Delete Entry {entry['id']}"):
                    vault_manager.delete_entry(entry['id'])
                    st.warning("Entry deleted! Please refresh to see changes.")
                # Flashcard management
                st.write("Flashcards:")
                for card in vault_manager.get_flashcards_for_entry(entry['id']):
                    with st.expander(f"Q: {card['question']}"):
                        st.write(f"A: {card['answer']}")
                        with st.form(f"edit_card_{card['id']}"):
                            new_q = st.text_input("Edit Question", value=card['question'])
                            new_a = st.text_input("Edit Answer", value=card['answer'])
                            c_sub = st.form_submit_button("Save Card Changes")
                            if c_sub:
                                vault_manager.edit_flashcard(card['id'], question=new_q, answer=new_a)
                                st.success("Flashcard updated! Please refresh to see changes.")
                        if st.button(f"Delete Flashcard {card['id']}"):
                            vault_manager.delete_flashcard(card['id'])
                            st.warning("Flashcard deleted! Please refresh to see changes.")
        
        # Additional analytics
        st.subheader("Reviews Per Day")
        all_reviews = []
        for card in vault_manager.flashcards:
            for review in card.get('reviews', []):
                all_reviews.append(review['date'][:10])
        if all_reviews:
            review_df = pd.DataFrame({'date': all_reviews})
            review_counts = review_df['date'].value_counts().sort_index()
            fig = px.bar(x=review_counts.index, y=review_counts.values, labels={'x': 'Date', 'y': 'Reviews'}, title='Reviews Per Day')
            st.plotly_chart(fig)
        
        st.subheader("Review Quality Distribution")
        qualities = []
        for card in vault_manager.flashcards:
            for review in card.get('reviews', []):
                qualities.append(review['quality'])
        if qualities:
            q_df = pd.DataFrame({'quality': qualities})
            fig = px.histogram(q_df, x='quality', nbins=6, title='Review Quality Distribution')
            st.plotly_chart(fig)
    
    # Notifications/Reminders placeholder
    st.subheader("Reminders & Notifications")
    due_cards = vault_manager.get_due_flashcards()
    if due_cards:
        st.info(f"You have {len(due_cards)} flashcards due for review today!")
    else:
        st.success("No reviews due today. Great job!")

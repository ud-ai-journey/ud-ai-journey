import streamlit as st
from title_optimizer import optimize_title

    # Streamlit page configuration
st.set_page_config(page_title="YouTube Title Optimizer 🎥", page_icon="📈", layout="centered")

    # Title and description
st.title("🎥 YouTube Title Optimizer")
st.markdown("Optimize your YouTube video titles with AI! Enter your title and description below to get an engaging, SEO-friendly title, alternate suggestions, and insights.")

    # User inputs
with st.form(key="title_form"):
        original_title = st.text_input("Current Video Title", placeholder="e.g., My First Vlog in Paris")
        description = st.text_area("Video Description", placeholder="e.g., Join me on my first vlog as I explore the beautiful city of Paris!", height=100)
        category = st.selectbox("Content Category", ["Tech", "Vlog", "Tutorial", "Gaming", "Lifestyle", "Other"])  # Bonus: Category dropdown
        submit_button = st.form_submit_button("Optimize Title 🚀")

    # Process the input and display results
if submit_button:
        if not original_title or not description:
            st.error("⚠️ Please provide both a title and description!")
        else:
            with st.spinner("Optimizing your title with AI..."):
                try:
                    result = optimize_title(original_title, description, category)
                    if result:
                        improved_title, alternates, reason = result

                        # Display the improved title
                        st.subheader("✨ Optimized Title")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{improved_title}**")
                        with col2:
                            st.button("📋 Copy", key="copy_improved", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{improved_title}");</script>', unsafe_allow_html=True))  # Bonus: Copy to Clipboard

                        # Display alternate suggestions
                        st.subheader("🔄 Alternate Title Suggestions")
                        for i, alt_title in enumerate(alternates, 1):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"{i}. {alt_title}")
                            with col2:
                                st.button("📋 Copy", key=f"copy_alt_{i}", on_click=lambda t=alt_title: st.write(f'<script>navigator.clipboard.writeText("{t}");</script>', unsafe_allow_html=True))  # Bonus: Copy to Clipboard

                        # Display reasoning
                        st.subheader("📝 Why This Title Works")
                        st.markdown(reason)
                    else:
                        st.error("❌ Failed to optimize title. Please check your API key or try again.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

    # Footer
st.markdown("---")
st.markdown("**Built by Boya Uday Kumar** | Part of 100 Days of Python + AI Challenge | June 2025")
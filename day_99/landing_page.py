import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def show_landing_page():
    """Show the main landing page"""
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 4rem; color: #1f77b4; margin-bottom: 1rem;">⚡ Energy Lens</h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">
            Discover your energy patterns to optimize productivity
        </p>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 1rem; color: white;">
            <h2 style="margin-bottom: 1rem;">🎯 Track • Analyze • Optimize</h2>
            <p style="font-size: 1.2rem;">Use AI-powered computer vision to discover your true productivity rhythms</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## 🚀 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📸 **Smart Detection**
        Take a photo or upload an image for instant energy analysis using advanced computer vision
        """)
    
    with col2:
        st.markdown("""
        ### 📊 **Pattern Analysis**
        Discover your peak performance times, energy dips, and weekly productivity patterns
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 **Actionable Insights**
        Get personalized recommendations to optimize your schedule and boost productivity
        """)
    
    # Demo Section
    st.markdown("## 🎨 See It In Action")
    
    # Create demo chart
    demo_data = pd.DataFrame({
        'Time': ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM'],
        'Energy': [2, 3, 3, 2, 1, 2, 3, 2],
        'Energy_Level': ['Medium', 'High', 'High', 'Medium', 'Low', 'Medium', 'High', 'Medium']
    })
    
    fig = px.line(demo_data, x='Time', y='Energy', 
                  title="📈 Your Energy Pattern (Demo)",
                  labels={'Energy': 'Energy Level (1=Low, 2=Medium, 3=High)'})
    
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Benefits Section
    st.markdown("## 💡 Why Energy Lens?")
    
    benefits = [
        "🔒 **Privacy-First**: All processing happens locally, no data sent to cloud",
        "🎯 **Actionable Insights**: Get specific recommendations for your schedule",
        "📱 **Easy to Use**: Just take a photo or upload an image",
        "📊 **Beautiful Visualizations**: See your patterns clearly",
        "🚀 **LinkedIn Ready**: Generate shareable insights automatically",
        "⚡ **Real-Time Analysis**: Instant energy detection and feedback"
    ]
    
    for benefit in benefits:
        st.markdown(f"• {benefit}")
    
    # CTA Section
    st.markdown("## 🚀 Ready to Discover Your Patterns?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Start Tracking Now", type="primary", use_container_width=True):
            st.success("🎯 Energy tracking ready! Use the navigation menu above to access the tracker.")
    
    with col2:
        if st.button("📖 Learn More", use_container_width=True):
            st.info("Features coming soon! Stay tuned for more energy optimization tools.")
    
    # Social Proof
    st.markdown("## 👥 What Users Are Saying")
    
    testimonials = [
        {
            "name": "Sarah K.",
            "role": "Product Manager",
            "quote": "Energy Lens helped me discover I'm most creative at 2 PM, not 9 AM!",
            "improvement": "35% productivity boost"
        },
        {
            "name": "Mike R.",
            "role": "Software Developer",
            "quote": "Finally understand why I struggle with afternoon meetings.",
            "improvement": "Better meeting scheduling"
        },
        {
            "name": "Lisa T.",
            "role": "Freelance Designer",
            "quote": "The insights are spot-on. I now block my peak hours for important work.",
            "improvement": "40% more focused time"
        }
    ]
    
    for testimonial in testimonials:
        with st.container():
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;">
                <p style="font-style: italic; margin-bottom: 1rem;">"{testimonial['quote']}"</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{testimonial['name']}</strong><br>
                        <small>{testimonial['role']}</small>
                    </div>
                    <div style="background: #2ecc71; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem;">
                        {testimonial['improvement']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>⚡ Energy Lens - Day 96 of 100 Days Python & AI Challenge</p>
        <p>Built with ❤️ using Streamlit, DeepFace, and Computer Vision</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_landing_page() 
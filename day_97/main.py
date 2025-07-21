import streamlit as st
from landing_page import show_landing_page
from app import main as show_main_app
from user_profile import show_user_profile

# Page config
st.set_page_config(
    page_title="Energy Lens - Pattern Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main navigation function"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: #1f77b4;">⚡ Energy Lens</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🧭 Navigation")
        
        # Navigation options
        page = st.radio(
            "Choose a page:",
            ["🏠 Home", "🎯 Energy Tracker", "👤 Your Profile"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick stats (if available)
        if page != "🏠 Home":
            try:
                from data_manager import DataManager
                data_manager = DataManager()
                energy_data = data_manager.get_energy_data()
                
                if not energy_data.empty:
                    st.markdown("### 📊 Quick Stats")
                    st.metric("Total Readings", len(energy_data))
                    high_energy_pct = (energy_data['energy_level'] == 'High').mean() * 100
                    st.metric("High Energy %", f"{high_energy_pct:.1f}%")
            except:
                pass
    
    # Page routing
    if page == "🏠 Home":
        show_landing_page()
    
    elif page == "🎯 Energy Tracker":
        show_main_app()
    
    elif page == "👤 Your Profile":
        show_user_profile()

if __name__ == "__main__":
    main() 
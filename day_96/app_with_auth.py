import streamlit as st
import pandas as pd
from auth_system import AuthSystem
from new_landing_page import show_new_landing_page
from new_main import show_authenticated_app
from energy_detector import EnergyDetector
from pattern_analyzer import PatternAnalyzer
from insights_generator import InsightsGenerator

# Page config
st.set_page_config(
    page_title="Energy Lens - Your Personal Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main app with authentication and navigation"""
    
    # Initialize auth system
    auth = AuthSystem()
    
    # Check if user is authenticated
    current_user = auth.get_current_user()
    
    if not current_user:
        # Show landing page with login
        show_new_landing_page()
    else:
        # User is authenticated - show main app
        energy_detector = EnergyDetector()
        pattern_analyzer = PatternAnalyzer()
        insights_generator = InsightsGenerator()
        
        show_authenticated_app(auth, current_user, energy_detector, pattern_analyzer, insights_generator)

if __name__ == "__main__":
    main() 
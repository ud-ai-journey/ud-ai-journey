import streamlit as st
import pandas as pd
from datetime import datetime
from energy_lens_app import AuthSystem

def debug_data():
    """Debug data functionality"""
    
    st.title("🔍 Data Debug")
    
    auth = AuthSystem()
    
    # Test user creation
    if st.button("Create Test User"):
        user_id = auth.login_user("test@debug.com", "Test User")
        st.success(f"Created user with ID: {user_id}")
    
    # Test data saving
    if st.button("Save Test Data"):
        auth.login_user("test@debug.com", "Test User")
        success = auth.save_energy_record("High", 85.0)
        if success:
            st.success("Test data saved!")
        else:
            st.error("Failed to save test data")
    
    # Test data retrieval
    if st.button("Get User Data"):
        auth.login_user("test@debug.com", "Test User")
        energy_data = auth.get_user_energy_data()
        
        st.write("Raw data:")
        st.write(energy_data)
        
        if not energy_data.empty:
            st.write("Data types:")
            st.write(energy_data.dtypes)
            
            st.write("Sample timestamps:")
            st.write(energy_data['timestamp'].head())
        else:
            st.warning("No data found")

if __name__ == "__main__":
    debug_data() 
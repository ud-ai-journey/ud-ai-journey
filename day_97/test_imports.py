import streamlit as st

st.title("🔍 Import Test")

try:
    from energy_detector import EnergyDetector
    st.success("✅ EnergyDetector imported successfully")
except Exception as e:
    st.error(f"❌ EnergyDetector import failed: {e}")

try:
    from pattern_analyzer import PatternAnalyzer
    st.success("✅ PatternAnalyzer imported successfully")
except Exception as e:
    st.error(f"❌ PatternAnalyzer import failed: {e}")

try:
    from insights_generator import InsightsGenerator
    st.success("✅ InsightsGenerator imported successfully")
except Exception as e:
    st.error(f"❌ InsightsGenerator import failed: {e}")

try:
    from energy_lens_app import AuthSystem
    st.success("✅ AuthSystem imported successfully")
except Exception as e:
    st.error(f"❌ AuthSystem import failed: {e}")

# Test data functionality
if st.button("Test Data Flow"):
    try:
        from energy_lens_app import AuthSystem
        auth = AuthSystem()
        
        # Test user creation
        user_id = auth.login_user("test@import.com", "Test User")
        st.success(f"✅ User created: {user_id}")
        
        # Test data saving
        success = auth.save_energy_record("High", 85.0)
        if success:
            st.success("✅ Data saved successfully")
        else:
            st.error("❌ Data save failed")
        
        # Test data retrieval
        energy_data = auth.get_user_energy_data()
        if not energy_data.empty:
            st.success(f"✅ Data retrieved: {len(energy_data)} records")
            st.write("Sample data:")
            st.write(energy_data.head())
        else:
            st.warning("⚠️ No data found")
            
    except Exception as e:
        st.error(f"❌ Data flow test failed: {e}") 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import uuid
from datetime import datetime
import base64
from io import BytesIO

from config import Config
from ai_engine import AIEngine
from data_manager import DataManager

# Page configuration
st.set_page_config(
    page_title="AI Relocation Guide",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    config = Config()
    ai_engine = AIEngine()
    data_manager = DataManager()
    return config, ai_engine, data_manager

config, ai_engine, data_manager = init_components()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .personality-score {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state management
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'current_step' not in st.session_state:
    st.session_state.current_step = 'welcome'

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

if 'personality_scores' not in st.session_state:
    st.session_state.personality_scores = {}

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Main navigation - PROGRESSIVE UNLOCK SYSTEM
def main_navigation():
    st.sidebar.title("🏠 AI Relocation Guide")
    
    # Define pages in order with unlock conditions
    pages = [
        ("🏠 Welcome", "welcome", lambda: True),  # Always unlocked
        ("📊 Personality Assessment", "personality", lambda: True),  # Always unlocked
        ("👤 Profile Setup", "profile", lambda: st.session_state.get("personality_complete", False)),
        ("🔍 City Recommendations", "recommendations", lambda: st.session_state.get("user_profile", {})),
        ("⚖️ City Comparison", "comparison", lambda: st.session_state.get("recommendations", [])),
        ("💰 Cost Analysis", "cost_analysis", lambda: st.session_state.get("recommendations", [])),
        ("📈 Insights & Analytics", "analytics", lambda: st.session_state.get("recommendations", [])),
        ("💾 Export Data", "export", lambda: st.session_state.get("recommendations", []) or st.session_state.get("user_profile", {}))
    ]
    
    # Simple navigation buttons with progressive unlock
    st.sidebar.markdown("### Navigation")
    
    for page_name, page_id, unlock_condition in pages:
        # Determine if this page is current
        is_current = st.session_state.current_step == page_id
        
        # Check if page is unlocked
        is_unlocked = unlock_condition()
        
        # Create button with different styling based on state
        if is_current:
            st.sidebar.markdown(f"**{page_name}** ✅")
        elif is_unlocked:
            if st.sidebar.button(page_name, key=f"nav_{page_id}"):
                st.session_state.current_step = page_id
                st.rerun()
        else:
            # Show disabled/locked page
            st.sidebar.markdown(f"🔒 {page_name} (Complete previous steps)")
    
    # Progress indicator - SIMPLIFIED
    current_index = next((i for i, (_, page_id, _) in enumerate(pages) if page_id == st.session_state.current_step), 0)
    progress = (current_index + 1) / len(pages)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Progress")
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Step {current_index + 1} of {len(pages)}")
    
    if current_index + 1 == len(pages):
        if st.session_state.get("journey_completed", False):
            st.sidebar.success("🎉 Journey Completed!")
        else:
            st.sidebar.success("✅ Completed!")

# Welcome page
def welcome_page():
    st.markdown('<h1 class="main-header">🏠 AI Relocation Guide</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Your AI-Powered Journey to the Perfect City
        
        Welcome to the most comprehensive relocation guide powered by artificial intelligence. 
        We'll help you find the perfect city that matches your personality, career goals, and lifestyle preferences.
        
        **What we'll discover together:**
        - 🧠 Your personality profile and city compatibility
        - 💼 Career opportunities in your field
        - 💰 Detailed cost of living analysis
        - 🌟 Cultural and lifestyle fit
        - 📊 Data-driven city comparisons
        
        Ready to start your journey? Let's begin with a quick personality assessment!
        """)
        
        if st.button("🚀 Start Your Journey", type="primary", use_container_width=True):
            go_to_step("personality")

# Personality assessment page
def personality_page():
    st.markdown('<h2 class="sub-header">🧠 Personality Assessment</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Let's understand your personality and preferences to find cities that truly match who you are.
    This assessment will help us identify the best cities for your lifestyle and career goals.
    """)
    
    questions = data_manager.get_personality_questions()
    
    if 'personality_answers' not in st.session_state:
        st.session_state.personality_answers = [-1] * len(questions)
    
    # Display questions
    for i, question in enumerate(questions):
        st.markdown(f"**Question {i+1}:** {question['question']}")
        
        answer = st.radio(
            f"Select your answer:",
            question['options'],
            key=f"q{i}",
            index=st.session_state.personality_answers[i] if st.session_state.personality_answers[i] >= 0 else 0
        )
        
        st.session_state.personality_answers[i] = question['options'].index(answer)
        st.divider()
    
    # Calculate scores when all questions are answered
    if all(answer >= 0 for answer in st.session_state.personality_answers):
        if st.button("📊 Calculate My Personality Profile", type="primary"):
            personality_scores = ai_engine.calculate_personality_scores(st.session_state.personality_answers)
            st.session_state.personality_scores = personality_scores
            st.session_state.personality_complete = True  # Set flag to indicate completion

    # Show results if personality assessment is complete
    if st.session_state.get("personality_complete", False):
        personality_scores = st.session_state.personality_scores
        
        # Display personality scores
        st.markdown("### Your Personality Profile")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Openness", f"{personality_scores['openness']:.0f}")
        with col2:
            st.metric("Conscientiousness", f"{personality_scores['conscientiousness']:.0f}")
        with col3:
            st.metric("Extraversion", f"{personality_scores['extraversion']:.0f}")
        with col4:
            st.metric("Agreeableness", f"{personality_scores['agreeableness']:.0f}")
        with col5:
            st.metric("Neuroticism", f"{personality_scores['neuroticism']:.0f}")
        
        # Personality radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[personality_scores['openness'], personality_scores['conscientiousness'], 
               personality_scores['extraversion'], personality_scores['agreeableness'], 
               personality_scores['neuroticism']],
            theta=['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism'],
            fill='toself',
            name='Your Profile'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Your Personality Profile"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("✅ Personality assessment complete! Let's set up your profile.")
        
        if st.button("👤 Continue to Profile Setup", type="primary"):
            go_to_step("profile")

# Profile setup page
def profile_page():
    st.markdown('<h2 class="sub-header">👤 Profile Setup</h2>', unsafe_allow_html=True)
    
    st.markdown("Tell us about your current situation and preferences to get personalized recommendations.")
    
    with st.form("profile_form"):
        st.subheader("Current Situation")
        
        current_city = st.text_input("Current City", placeholder="e.g., New York, NY")
        current_salary = st.number_input("Current Annual Salary ($)", min_value=20000, max_value=500000, value=75000, step=5000)
        
        st.subheader("Career Information")
        career_field = st.selectbox("Career Field", config.CAREER_CATEGORIES)
        years_experience = st.slider("Years of Experience", 0, 20, 5)
        
        st.subheader("Preferences")
        preferred_climate = st.selectbox("Preferred Climate", [
            "Warm and sunny year-round",
            "Four distinct seasons", 
            "Mild temperatures",
            "I can adapt to any climate"
        ])
        
        lifestyle_priority = st.selectbox("Most Important Factor", [
            "Career opportunities",
            "Cost of living",
            "Cultural activities",
            "Outdoor recreation",
            "Family-friendly environment"
        ])
        
        budget_preference = st.selectbox("Budget Preference", [
            "Affordable - willing to compromise on amenities",
            "Balanced - good value for money",
            "Premium - willing to pay more for quality"
        ])
        
        submitted = st.form_submit_button("📊 Get Recommendations", type="primary")
        
        if submitted:
            # Create user profile
            user_profile = {
                'current_city': current_city,
                'current_salary': current_salary,
                'career_info': {
                    'field': career_field,
                    'years_experience': years_experience
                },
                'preferences': {
                    'climate': preferred_climate,
                    'lifestyle_priority': lifestyle_priority,
                    'budget_preference': budget_preference
                },
                'personality_scores': st.session_state.personality_scores
            }
            
            st.session_state.user_profile = user_profile
            # Save session after profile setup
            data_manager.save_user_session(
                st.session_state.session_id,
                {
                    "user_profile": st.session_state.get("user_profile", {}),
                    "personality_scores": st.session_state.get("personality_scores", {}),
                    "recommendations": st.session_state.get("recommendations", []),
                    "comparisons": st.session_state.get("comparison_data", []),
                    "cost_analysis": st.session_state.get("cost_analysis", {})
                }
            )
            with st.spinner("🤖 AI is analyzing cities for you..."):
                recommendations = ai_engine.get_recommendations(user_profile, 5)
                st.session_state.recommendations = recommendations
            
            st.success("✅ Profile created and recommendations generated!")
            go_to_step("recommendations")

# Recommendations page
def recommendations_page():
    st.markdown('<h2 class="sub-header">🔍 Your City Recommendations</h2>', unsafe_allow_html=True)
    
    if not st.session_state.recommendations:
        st.warning("Please complete the personality assessment and profile setup first.")
        return
    
    st.markdown("Based on your personality and preferences, here are your top city matches:")
    
    # Display recommendations
    for i, rec in enumerate(st.session_state.recommendations):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {i+1}. {rec['city_name']}")
                
                # Get city data for detailed info
                city_data = data_manager.get_city_by_name(rec['city_name'])
                if city_data:
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Cost of Living", f"${sum(city_data['cost_of_living'].values()):,}/month")
                        st.metric("Avg Salary", f"${city_data['career']['avg_salary']:,}")
                    
                    with col_b:
                        st.metric("Walkability", f"{city_data['lifestyle']['walkability']}/100")
                        st.metric("Safety Score", f"{city_data['lifestyle']['safety_score']}/100")
                    
                    with col_c:
                        st.metric("Diversity", f"{city_data['culture']['diversity_score']}/100")
                        st.metric("Arts Scene", f"{city_data['culture']['arts_score']}/100")
            
            with col2:
                st.markdown(f"<div class='personality-score'>{rec['compatibility_score']:.0f}% Match</div>", 
                           unsafe_allow_html=True)
            
            # Show AI analysis
            with st.expander("🤖 AI Analysis"):
                st.write(rec['analysis'])
            
            st.divider()
    
    # Save session after recommendations
    data_manager.save_user_session(
        st.session_state.session_id,
        {
            "user_profile": st.session_state.get("user_profile", {}),
            "personality_scores": st.session_state.get("personality_scores", {}),
            "recommendations": st.session_state.get("recommendations", []),
            "comparisons": st.session_state.get("comparison_data", []),
            "cost_analysis": st.session_state.get("cost_analysis", {})
        }
    )
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ Compare Cities", type="primary"):
            go_to_step("comparison")
    
    with col2:
        if st.button("💰 Cost Analysis", type="primary"):
            go_to_step("cost_analysis")

# City comparison page
def comparison_page():
    st.markdown('<h2 class="sub-header">⚖️ City Comparison</h2>', unsafe_allow_html=True)
    
    st.markdown("Compare specific cities side by side to make informed decisions.")
    
    # City selection
    cities = data_manager.get_cities()
    city_names = [city['name'] for city in cities]
    
    col1, col2 = st.columns(2)
    
    with col1:
        city1 = st.selectbox("Select First City", city_names, index=0)
    
    with col2:
        city2 = st.selectbox("Select Second City", city_names, index=1)
    
    # Always show navigation buttons
    st.markdown("---")
    nav1, nav2 = st.columns(2)
    
    with nav1:
        if st.button("💰 Cost Analysis", type="primary"):
            go_to_step("cost_analysis")
    
    with nav2:
        if st.button("📈 Analytics", type="primary"):
            go_to_step("analytics")
    
    if st.button("🔄 Compare Cities", type="primary"):
        if city1 == city2:
            st.error("Please select different cities for comparison.")
        else:
            # Get city data
            city1_data = data_manager.get_city_by_name(city1)
            city2_data = data_manager.get_city_by_name(city2)
            
            if city1_data and city2_data:
                # Create comparison
                comparison_data = {
                    'city1': city1_data,
                    'city2': city2_data
                }
                
                st.session_state.comparison_data = comparison_data
                
                # Save session after comparison
                data_manager.save_user_session(
                    st.session_state.session_id,
                    {
                        "user_profile": st.session_state.get("user_profile", {}),
                        "personality_scores": st.session_state.get("personality_scores", {}),
                        "recommendations": st.session_state.get("recommendations", []),
                        "comparisons": st.session_state.get("comparison_data", []),
                        "cost_analysis": st.session_state.get("cost_analysis", {})
                    }
                )
                
                # Display comparison
                display_city_comparison(city1_data, city2_data)

def display_city_comparison(city1, city2):
    st.markdown(f"## {city1['name']} vs {city2['name']}")
    
    # Cost comparison
    st.subheader("💰 Cost of Living Comparison")
    
    cost_categories = list(city1['cost_of_living'].keys())
    city1_costs = [city1['cost_of_living'][cat] for cat in cost_categories]
    city2_costs = [city2['cost_of_living'][cat] for cat in cost_categories]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name=city1['name'], x=cost_categories, y=city1_costs))
    fig.add_trace(go.Bar(name=city2['name'], x=cost_categories, y=city2_costs))
    
    fig.update_layout(
        title="Monthly Cost Comparison",
        barmode='group',
        xaxis_title="Cost Categories",
        yaxis_title="Monthly Cost ($)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Lifestyle comparison
    st.subheader("🌟 Lifestyle Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{city1['name']}**")
        st.metric("Walkability", f"{city1['lifestyle']['walkability']}/100")
        st.metric("Public Transit", f"{city1['lifestyle']['public_transit']}/100")
        st.metric("Safety", f"{city1['lifestyle']['safety_score']}/100")
        st.metric("Parks", f"{city1['lifestyle']['parks_score']}/100")
    
    with col2:
        st.markdown(f"**{city2['name']}**")
        st.metric("Walkability", f"{city2['lifestyle']['walkability']}/100")
        st.metric("Public Transit", f"{city2['lifestyle']['public_transit']}/100")
        st.metric("Safety", f"{city2['lifestyle']['safety_score']}/100")
        st.metric("Parks", f"{city2['lifestyle']['parks_score']}/100")
    
    # Career comparison
    st.subheader("💼 Career Opportunities")
    
    career_metrics = ['tech_jobs', 'finance_jobs', 'healthcare_jobs', 'education_jobs']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name=city1['name'], x=career_metrics, y=[city1['career'][m] for m in career_metrics]))
    fig.add_trace(go.Bar(name=city2['name'], x=career_metrics, y=[city2['career'][m] for m in career_metrics]))
    
    fig.update_layout(
        title="Career Opportunity Scores",
        barmode='group',
        xaxis_title="Career Fields",
        yaxis_title="Opportunity Score"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Cost analysis page
def cost_analysis_page():
    st.markdown('<h2 class="sub-header">💰 Cost Analysis</h2>', unsafe_allow_html=True)
    st.markdown("Analyze the financial impact of moving to different cities.")

    user_profile = st.session_state.user_profile
    cities = data_manager.get_cities()
    city_names = [city['name'] for city in cities]

    # Fallback: let user select current city if not set
    current_city = user_profile.get('current_city', '')
    if not current_city:
        st.warning("Please select your current city to proceed.")
        current_city = st.selectbox("Select Your Current City", city_names, key="current_city_cost_analysis")
    current_salary = user_profile.get('current_salary', 75000)

    target_city = st.selectbox("Select Target City for Analysis", city_names, key="target_city_cost_analysis")

    if st.button("📊 Analyze Cost Impact", type="primary"):
        if current_city and target_city:
            cost_analysis = ai_engine.generate_cost_analysis(current_city, target_city, current_salary)
            st.session_state.cost_analysis = cost_analysis
            # Save session after cost analysis
            data_manager.save_user_session(
                st.session_state.session_id,
                {
                    "user_profile": st.session_state.get("user_profile", {}),
                    "personality_scores": st.session_state.get("personality_scores", {}),
                    "recommendations": st.session_state.get("recommendations", []),
                    "comparisons": st.session_state.get("comparison_data", []),
                    "cost_analysis": st.session_state.get("cost_analysis", {})
                }
            )
            if 'error' not in cost_analysis:
                display_cost_analysis(cost_analysis)
            else:
                st.error("Unable to generate cost analysis. Please check city names.")
        else:
            st.error("Please provide both current and target cities.")

def display_cost_analysis(analysis):
    st.markdown(f"## Cost Analysis: {analysis['current_city']} → {analysis['target_city']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Cost Change", f"${analysis['total_monthly_change']:+,.0f}")
    with col2:
        st.metric("Percentage Change", f"{analysis['total_percentage_change']:+.1f}%")
    with col3:
        st.metric("Salary Adjustment Needed", f"${analysis['salary_adjustment_needed']:+,.0f}")
    st.subheader("📊 Detailed Cost Breakdown")
    cost_data = []
    for category, data in analysis['cost_changes'].items():
        cost_data.append({
            'Category': category.title(),
            'Current': data['current'],
            'Target': data['target'],
            'Change': data['change'],
            'Percentage': data['percentage_change']
        })
    df = pd.DataFrame(cost_data)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Current',
        x=df['Category'],
        y=df['Current'],
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        name='Target',
        x=df['Category'],
        y=df['Target'],
        marker_color='orange'
    ))
    fig.update_layout(
        title="Monthly Cost Comparison by Category",
        barmode='group',
        xaxis_title="Cost Categories",
        yaxis_title="Monthly Cost ($)"
    )
    st.plotly_chart(fig, use_container_width=True)
    if analysis['recommendations']:
        st.subheader("💡 Recommendations")
        for rec in analysis['recommendations']:
            st.info(rec)
    
    # Manual button to continue to analytics - SIMPLE SOLUTION
    st.markdown("---")
    st.success("✅ Cost analysis completed!")
    
    # Force analytics page with direct session state change
    if st.button("📈 Continue to Insights & Analytics", key="cost_to_analytics_btn", type="primary", use_container_width=True):
        st.success("🔍 Button clicked! Setting analytics...")
        st.session_state.current_step = "analytics"
        st.session_state.force_analytics = True
        st.info(f"Current step will be: {st.session_state.current_step}")
        st.rerun()
    
    if st.button("🏠 Start Over", type="primary"):
        st.session_state.current_step = "welcome"
        st.rerun()

# Analytics page - ULTRA SIMPLE VERSION
def analytics_page():
    st.success("🎉 SUCCESS! You've reached the Analytics page!")
    
    st.markdown('<h2 class="sub-header">📈 Insights & Analytics</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Page Status")
    st.info("✅ **ANALYTICS PAGE IS WORKING!**")
    st.info(f"Current step: {st.session_state.current_step}")
    
    st.markdown("### 📊 Sample Analytics Content")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cities", "25")
    with col2:
        st.metric("Avg Cost", "$3,200")
    with col3:
        st.metric("Top City", "Austin, TX")
    with col4:
        st.metric("Success Rate", "95%")
    
    # Sample chart
    st.markdown("### 📈 Sample Chart")
    sample_data = pd.DataFrame({
        'City': ['Austin', 'Seattle', 'Denver', 'Portland', 'Nashville'],
        'Score': [85, 82, 78, 75, 72]
    })
    
    fig = px.bar(sample_data, x='City', y='Score', title="Sample City Rankings")
    st.plotly_chart(fig, use_container_width=True)
    
    # Navigation
    st.markdown("---")
    st.success("✅ Analytics completed!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Continue to Export Data", type="primary", use_container_width=True):
            st.session_state.current_step = "export"
            st.rerun()
    with col2:
        if st.button("🏠 Start Over", type="primary"):
            st.session_state.current_step = "welcome"
            st.rerun()

def display_city_ranking(title, cities):
    st.markdown(f"### {title}")
    
    # Create a unique identifier for this ranking category
    category_id = title.lower().replace(' ', '_').replace('&', 'and')
    
    for i, city in enumerate(cities):
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{i+1}. {city['name']}**")
                st.caption(f"{city['state']}")
            
            with col2:
                if 'cost' in title.lower():
                    total_cost = sum(city['cost_of_living'].values())
                    st.metric("Monthly Cost", f"${total_cost:,}")
                elif 'career' in title.lower():
                    st.metric("Avg Salary", f"${city['career']['avg_salary']:,}")
                elif 'lifestyle' in title.lower():
                    lifestyle_score = (city['lifestyle']['walkability'] + city['lifestyle']['safety_score']) / 2
                    st.metric("Lifestyle Score", f"{lifestyle_score:.0f}/100")
                elif 'culture' in title.lower():
                    culture_score = (city['culture']['diversity_score'] + city['culture']['arts_score'] + city['culture']['nightlife_score']) / 3
                    st.metric("Culture Score", f"{culture_score:.0f}/100")
            
            with col3:
                # Create a unique key using city ID or name with better sanitization
                city_name_clean = city['name'].replace(' ', '_').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                city_key = f"view_{category_id}_{city_name_clean}_{i}"
                if st.button(f"View Details", key=city_key):
                    st.session_state.selected_city = city
                    st.rerun()

def clear_session_and_restart():
    for key in [
        "current_step", "user_profile", "personality_scores", "recommendations",
        "comparison_data", "cost_analysis", "personality_answers", "personality_complete"
    ]:
        if key in st.session_state:
            del st.session_state[key]
    go_to_step("welcome")

# Export page
def export_page():
    st.markdown('<h2 class="sub-header">💾 Export Your Data</h2>', unsafe_allow_html=True)
    st.markdown("Download your relocation analysis and recommendations for future reference.")
    
    # Show completion celebration if journey is completed
    if st.session_state.get("journey_completed", False):
        st.success("🎉 Congratulations! You've completed your AI Relocation Journey!")
        st.markdown("### 🏆 Journey Summary")
        st.markdown("You've successfully:")
        st.markdown("- ✅ Completed personality assessment")
        st.markdown("- ✅ Set up your profile")
        st.markdown("- ✅ Received city recommendations")
        st.markdown("- ✅ Analyzed costs and insights")
        st.markdown("- ✅ Downloaded your relocation data")
        st.markdown("**Your relocation journey is complete!** 🚀")

    # Try to get data from data_manager, fallback to session_state
    export_data = data_manager.export_user_data(st.session_state.session_id)
    session_data = {
        "user_profile": st.session_state.get("user_profile", {}),
        "personality_scores": st.session_state.get("personality_scores", {}),
        "recommendations": st.session_state.get("recommendations", []),
        "comparisons": st.session_state.get("comparison_data", []),
        "cost_analysis": st.session_state.get("cost_analysis", {})
    }
    has_data = any([
        session_data["user_profile"],
        session_data["personality_scores"],
        session_data["recommendations"],
        session_data["comparisons"],
        session_data["cost_analysis"]
    ])
    if not has_data and export_data:
        has_data = True
        session_data = export_data
    if has_data:
        json_str = json.dumps(session_data, indent=2)
        col1, col2 = st.columns(2)
        with col1:
            if st.download_button(
                label="📄 Download JSON Report",
                data=json_str,
                file_name=f"relocation_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            ):
                # Mark as completed when user downloads
                st.session_state.journey_completed = True
                st.success("🎉 Congratulations! You've completed your AI Relocation Journey!")
                st.balloons()
        with col2:
            if session_data.get("recommendations"):
                df = pd.DataFrame(session_data["recommendations"])
                csv = df.to_csv(index=False)
                if st.download_button(
                    label="📊 Download CSV Report",
                    data=csv,
                    file_name=f"city_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                ):
                    # Mark as completed when user downloads
                    st.session_state.journey_completed = True
                    st.success("🎉 Congratulations! You've completed your AI Relocation Journey!")
                    st.balloons()
        st.subheader("📋 Export Summary")
        if session_data.get("personality_scores"):
            st.markdown("**Personality Profile:**")
            for dimension, score in session_data["personality_scores"].items():
                st.write(f"- {dimension.title()}: {score:.0f}/100")
        if session_data.get("recommendations"):
            st.markdown("**Top Recommendations:**")
            for i, rec in enumerate(session_data["recommendations"][:3]):
                st.write(f"{i+1}. {rec['city_name']} ({rec['compatibility_score']:.0f}% match)")
        if session_data.get("user_profile"):
            st.markdown("**Profile Information:**")
            profile = session_data["user_profile"]
            st.write(f"- Current City: {profile.get('current_city', 'N/A')}")
            st.write(f"- Current Salary: ${profile.get('current_salary', 0):,}")
            st.write(f"- Career Field: {profile.get('career_info', {}).get('field', 'N/A')}")
    else:
        st.warning("No data available for export. Please complete the assessment and profile setup first.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 Analytics", type="primary"):
            go_to_step("analytics")
    with col2:
        if st.button("🏠 Start Over", type="primary"):
            clear_session_and_restart()

# Main app
def main():

    
    main_navigation()
    
    # Route to appropriate page
    if st.session_state.current_step == "welcome":
        welcome_page()
    elif st.session_state.current_step == "personality":
        personality_page()
    elif st.session_state.current_step == "profile":
        profile_page()
    elif st.session_state.current_step == "recommendations":
        recommendations_page()
    elif st.session_state.current_step == "comparison":
        comparison_page()
    elif st.session_state.current_step == "cost_analysis":
        cost_analysis_page()
    elif st.session_state.current_step == "analytics" or st.session_state.get("force_analytics", False):
        # Debug: Show what triggered this
        st.sidebar.markdown(f"**Debug:** Analytics triggered - current_step: {st.session_state.current_step}, force_analytics: {st.session_state.get('force_analytics', False)}")
        
        # Clear the force flag
        if "force_analytics" in st.session_state:
            del st.session_state.force_analytics
        
        # Ensure we're on analytics
        st.session_state.current_step = "analytics"
        
        try:
            analytics_page()
        except Exception as e:
            st.error(f"Error loading analytics page: {str(e)}")
            st.info("Please try refreshing the page.")
            # Keep user on analytics page even if there's an error
            st.session_state.current_step = "analytics"
            st.rerun()
    elif st.session_state.current_step == "export":
        export_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        Built with ❤️ as part of the 100 Days of AI Journey | Powered by Streamlit & OpenAI
        </div>
        """,
        unsafe_allow_html=True
    )

def go_to_step(step):
    st.session_state.current_step = step
    st.rerun()

if __name__ == "__main__":
    main() 
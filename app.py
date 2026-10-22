import streamlit as st
import numpy as np
import pandas as pd
import json
import joblib
from soil_score import calculate_soil_score
from advisory import get_advisory_suggestions

# Page Configurations - Clean Wide Canvas
st.set_page_config(
    page_title="PrecisionSoil Matrix", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom Global CSS for Premium UI Components, Soft Shadows, and Hover Cards
st.markdown("""
    <style>
    /* Main Background Tweaks */
    .main { background-color: #fcfdfd; }
    div[data-testid="stSidebarUserContent"] { background-color: #f4f7f6; }
    
    /* Unified Input Container Card */
    .unified-card {
        background: #ffffff;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #eef2f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }
    
    /* Modern Dynamic Crop Cards */
    .crop-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 16px;
        border: 1px solid #eef2f0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.01);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .crop-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(4, 120, 87, 0.08);
        border-color: #a7f3d0;
    }
    
    /* Custom Tab Styling Overrides for Seamless Aesthetics */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f4f7f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: #4b5563;
    }
    .stTabs [aria-selected="true"] {
        background-color: #047857 !important;
        color: white !important;
        font-weight: 600;
    }

    /* Clean Divider Line */
    hr { margin-top: 1rem; margin-bottom: 1rem; border-color: #eef2f0; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ml_model():
    try: return joblib.load('model.pkl')
    except: return None

@st.cache_data
def load_lookup_table():
    try:
        with open('crop_lookup.json', 'r') as f: return json.load(f)
    except:
        return {}

model = load_ml_model()
crop_lookup = load_lookup_table()

# 1. Premium Command Center Header Banner
st.markdown("""
    <div style='background: linear-gradient(135deg, #064e3b 0%, #047857 100%); padding: 40px 30px; border-radius: 20px; text-align: center; margin-bottom: 35px; box-shadow: 0 10px 30px rgba(6,78,59,0.15);'>
        <span style='background: rgba(255,255,255,0.15); color: #a7f3d0; padding: 6px 16px; border-radius: 30px; font-size: 0.85em; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;'>AI Agro-Intelligence Engine</span>
        <h1 style='color: white; margin: 12px 0 6px 0; font-size: 3em; font-family: system-ui, -apple-system, sans-serif; font-weight: 800; letter-spacing: -0.5px;'>🛰️ PrecisionSoil Matrix</h1>
        <p style='color: #d1fae5; margin: 0; font-size: 1.2em; font-weight: 300; max-width: 700px; margin: 0 auto; opacity: 0.95;'>Advanced Data-Driven Soil Profiling & Predictive Crop Advisory Core</p>
    </div>
""", unsafe_allow_html=True)

# 2. Operational Parameter Controls (Left Sidebar Panel)
with st.sidebar:
    st.markdown("### 🗺️ Operational Parameters")
    st.markdown("Set local geographic variables to align machine learning patterns.")
    
    state_input = st.selectbox("Select Farm Location (State)", [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
        "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand", "Karnataka", 
        "Kerala", "Madhya Pradesh", "Maharashtra", "Meghalaya", "Odisha", "Punjab", 
        "Rajasthan", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ], index=10)
    
    season_input = st.selectbox("Cropping Season Timeline", ["Kharif", "Rabi", "Zaid"])
    soil_input = st.selectbox("Primary Structural Soil Profile", ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Loamy", "Clay"])
    budget_input = st.selectbox("Working Cost Allocation Tier", ["Low (< ₹10,000)", "Medium (₹10,000–₹50,000)", "High (> ₹50,000)"], index=1)
    
    budget_tier = "Low" if "Low" in budget_input else "Medium" if "Medium" in budget_input else "High"
    st.markdown("---")
    st.caption("⚙️ Framework updates matrix boundaries automatically upon filtering data nodes.")

# 3. Two Column Master Split
col1, col2 = st.columns([9, 10], gap="large")

with col1:
    # Stacking the entire matrix layout, including headers, into one unified aesthetic white box
    st.markdown("<div class='unified-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #064e3b; margin-top:0; margin-bottom:25px; font-weight:700;'>🧪 Diagnostic Core Entry Matrix</h3>", unsafe_allow_html=True)
    
    # Subsection A: Chemical Elements
    st.markdown("<h5 style='color: #374151; margin-top:0; margin-bottom:12px; font-weight:600;'>🧫 Chemical Macronutrient Quantities (kg/ha)</h5>", unsafe_allow_html=True)
    chem_col1, chem_col2, chem_col3 = st.columns(3)
    with chem_col1:
        n_input = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=90, step=5)
    with chem_col2:
        p_input = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=80, step=5)
    with chem_col3:
        k_input = st.number_input("Potassium (K)", min_value=0, max_value=300, value=100, step=5)
        
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
    
    # Subsection B: Environmental Variables
    st.markdown("<h5 style='color: #374151; margin-top:0; margin-bottom:12px; font-weight:600;'>🌤️ Atmospheric & Environmental Nodes</h5>", unsafe_allow_html=True)
    env_col1, env_col2, env_col3 = st.columns(3)
    with env_col1:
        temp_input = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=28.0, step=0.5)
    with env_col2:
        hum_input = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
    with env_col3:
        ph_input = st.number_input("Soil pH Factor", min_value=0.0, max_value=14.0, value=6.8, step=0.1)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    trigger_analysis = st.button("🚀 Execute Precision Soil Diagnosis", use_container_width=True, type="primary")

with col2:
    st.markdown("### 🌡️ Analytical Diagnostics Engine")
    
    if model is None:
        st.error("Model artifacts missing. Please execute `train_model.py` inside your system terminal first!")
    else:
        # Evaluate Soil Rating
        score, label, color = calculate_soil_score(n_input, p_input, k_input, hum_input, ph_input)
        
        hex_colors = {"green": "#047857", "orange": "#d97706", "red": "#b91c1c"}
        bg_colors = {"green": "#f0fdf4", "orange": "#fffbeb", "red": "#fef2f2"}
        selected_color = hex_colors.get(color, "#047857")
        selected_bg = bg_colors.get(color, "#f0fdf4")
        
        # Dashboard Score Banner
        st.markdown(f"""
            <div style='background-color: {selected_bg}; padding: 25px; border-radius: 16px; border-left: 8px solid {selected_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.02); margin-bottom: 25px;'>
                <h4 style='margin: 0; color: #6b7280; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>Ratio-Balanced Soil Quality Score</h4>
                <div style='display: flex; align-items: baseline; margin: 8px 0;'>
                    <h1 style='margin: 0; color: {selected_color}; font-size: 3.5em; font-weight: 800; line-height: 1;'>{score}</h1>
                    <span style='font-size: 1.2em; color: #9ca3af; margin-left: 6px; font-weight: 500;'>/ 100</span>
                </div>
                <p style='margin: 4px 0 0 0; font-size: 1em; color: #374151;'>Matrix Health Evaluation: <span style='color: {selected_color}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>{label}</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🌾 Crop Optimization Models", "🛠️ Actionable Field Advisory"])
        
        with tab1:
            features = np.array([[n_input, p_input, k_input, temp_input, hum_input, ph_input]])
            probabilities = model.predict_proba(features)[0]
            class_labels = model.classes_
            
            top_indices = np.argsort(probabilities)[::-1][:4]
            top_4_crops = [class_labels[idx] for idx in top_indices]
            
            filtered_crops = []
            relaxation_applied = []
            
            def run_filter(b_constraint, s_constraint):
                matches = []
                for crop in top_4_crops:
                    if crop in crop_lookup:
                        meta = crop_lookup[crop]
                        if state_input in meta.get("regions", []) and season_input in meta.get("seasons", []):
                            if (not s_constraint or soil_input in meta.get("soil_types", [])) and (not b_constraint or budget_tier in meta.get("budget", [])):
                                matches.append(crop)
                    else:
                        matches.append(crop)
                return matches

            filtered_crops = run_filter(b_constraint=True, s_constraint=True)
            if len(filtered_crops) == 0:
                relaxation_applied.append("Cost Allocation Array")
                filtered_crops = run_filter(b_constraint=False, s_constraint=True)
            if len(filtered_crops) == 0:
                relaxation_applied.append("Soil Profile Matrix")
                filtered_crops = run_filter(b_constraint=False, s_constraint=False)
            
            if relaxation_applied:
                st.caption(f"ℹ️ *Note: Constraint layers relaxed for ({', '.join(relaxation_applied)}) to extract closest geographical fits.*")
            
            if filtered_crops:
                st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
                for idx, crop in enumerate(filtered_crops[:3]):
                    meta = crop_lookup.get(crop, {"budget": [budget_tier], "soil_types": [soil_input]})
                    
                    st.markdown(f"""
                        <div class='crop-card'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #064e3b; font-weight: 700; font-size: 1.2em; text-transform: capitalize;'>🏆 Rank #{idx+1}: {crop}</span>
                                <span style='background-color: #e6f4ea; color: #047857; padding: 4px 12px; border-radius: 20px; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Match Validated</span>
                            </div>
                            <hr>
                            <p style='margin: 0; color: #4b5563; font-size: 0.95em; line-height: 1.7;'>
                                <b style='color: #1f2937;'>💰 Required Budget Tier:</b> {', '.join(meta.get('budget', []))} <br>
                                <b style='color: #1f2937;'>🌱 Compatible Structural Soils:</b> {', '.join(meta.get('soil_types', []))}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Structural Boundary Clash: Neural recommendations conflict with ambient parameters inside {state_input} during {season_input}.")
        
        with tab2:
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            advisory_bullet_points = get_advisory_suggestions(n_input, p_input, k_input, hum_input, ph_input, label)
            for item in advisory_bullet_points:
                st.markdown(f"✨ {item}")

"""
DeepCommerce Analytics Dashboard
Modern retail analytics platform with traffic, localization, and heatmap analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="DeepCommerce Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PASSWORD AUTHENTICATION
# =====================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown("### 🔐 DeepCommerce Analytics")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.info("Please enter your password to access the dashboard.")
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("### 🔐 DeepCommerce Analytics")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is not True

# Custom CSS for modern design
st.markdown("""
    <style>
    /* ============================================= */
    /* 🔥 드롭다운 메뉴 - 최우선 가독성 (강제 적용) */
    /* ============================================= */
    
    /* 팝오버/메뉴 컨테이너 - 흰색 배경 강제 */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] > div,
    ul[role="listbox"],
    ul[data-testid="stVirtualDropdown"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
    }
    
    /* 드롭다운 옵션 - 검정 텍스트 강제 */
    li[role="option"],
    div[data-baseweb="menu"] li,
    ul[role="listbox"] li,
    ul[data-testid="stVirtualDropdown"] li,
    div[data-testid="stMarkdownContainer"] li {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    /* 옵션 내 모든 텍스트 */
    li[role="option"] *,
    div[data-baseweb="menu"] li *,
    ul[role="listbox"] li *,
    ul[data-testid="stVirtualDropdown"] li * {
        color: #000000 !important;
    }
    
    /* Hover 상태 */
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover {
        background-color: #e5e7eb !important;
        background: #e5e7eb !important;
        color: #000000 !important;
    }
    
    /* 선택된 값 표시 영역 */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    
    /* ============================================= */
    /* Main content area - White background */
    /* ============================================= */
    .main {
        padding: 0rem 1rem;
        background-color: white !important;
    }
    .stApp {
        background-color: white !important;
    }
    .main > div {
        background-color: white !important;
    }
    
    /* Main content text */
    h1, h2, h3 {
        color: #1f2937 !important;
    }
    p, div, span, label {
        color: #1f2937 !important;
    }
    
    /* ============================================= */
    /* Input 요소 스타일 */
    /* ============================================= */
    input, select, textarea, button {
        background-color: #e5e7eb !important;
        color: #111827 !important;
        border: 1px solid #9ca3af !important;
        font-weight: 600 !important;
    }
    
    /* Main content buttons */
    .main button, .main .stButton > button {
        background-color: #d1d5db !important;
        color: #111827 !important;
        border: 2px solid #6b7280 !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
    }
    .main button:hover, .main .stButton > button:hover {
        background-color: #9ca3af !important;
        border-color: #4b5563 !important;
    }
    .main button:active, .main .stButton > button:active {
        background-color: #6b7280 !important;
    }
    
    /* Main selectbox - 밝은 배경에 어두운 텍스트 */
    .main select,
    .main .stSelectbox > div > div,
    .main .stSelectbox [data-baseweb="select"],
    .main [data-baseweb="select"],
    .main [data-baseweb="select"] > div {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
        font-weight: 600 !important;
        border: 1px solid #d1d5db !important;
    }
    
    .main [data-baseweb="select"] input,
    .main [data-baseweb="select"] span {
        color: #111827 !important;
        background-color: transparent !important;
        font-weight: 600 !important;
    }
    
    .main [data-baseweb="select"] svg {
        color: #111827 !important;
        fill: #111827 !important;
    }
    
    /* Slider component */
    .main .stSlider > div > div {
        background-color: white !important;
    }
    .main .stSlider label {
        color: #1f2937 !important;
    }
    .main [role="slider"] {
        background-color: #3b82f6 !important;
    }
    
    /* Hide slider tick marks */
    .main [data-baseweb="slider"] [data-testid],
    .main [data-baseweb="slider"] > div:not([role="slider"]):not([class*="Thumb"]) {
        display: none !important;
    }
    .main .stSlider [data-baseweb="slider"] ~ div {
        display: none !important;
    }
    
    /* ============================================= */
    /* Sidebar - Dark background, Light text */
    /* ============================================= */
    [data-testid="stSidebar"] {
        background-color: #1f2937 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #f9fafb !important;
    }
    
    /* 🔥 Sidebar selectbox - 선택된 값 표시 (밝은 텍스트 강제) */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-baseweb="select"] div[role="button"],
    [data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] div {
        color: #f9fafb !important;
        background-color: #374151 !important;
    }
    
    /* Sidebar selectbox 내부 모든 텍스트 */
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #f9fafb !important;
    }
    
    /* Sidebar selectbox 배경 */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #374151 !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > label {
        color: #f9fafb !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #f9fafb !important;
    }
    
    /* Info box in sidebar */
    [data-testid="stSidebar"] .stAlert {
        background-color: #374151 !important;
        color: #f9fafb !important;
    }
    
    /* ============================================= */
    /* 🔥 추가 드롭다운 강제 스타일 (Streamlit 1.30+) */
    /* ============================================= */
    
    /* Streamlit 최신 버전 가상 드롭다운 */
    [data-testid="stVirtualDropdown"],
    [data-testid="stVirtualDropdown"] > div,
    [data-testid="stSelectboxVirtualDropdown"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
    }
    
    [data-testid="stVirtualDropdown"] [role="option"],
    [data-testid="stSelectboxVirtualDropdown"] [role="option"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-testid="stVirtualDropdown"] [role="option"]:hover,
    [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover {
        background-color: #f0f0f0 !important;
        background: #f0f0f0 !important;
    }
    
    /* 드롭다운 내 모든 div, span 강제 */
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] span,
    [data-baseweb="menu"] div,
    [data-baseweb="menu"] span {
        color: #000000 !important;
    }
    
    /* Metrics in main area */
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stMetric label {
        color: #4b5563 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1f2937 !important;
    }
    
    /* Hide default sidebar nav */
    div[data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Hide BaseWeb slider tooltips */
    div[data-baseweb="tooltip"],
    div[role="tooltip"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* Custom slider tooltip styling */
    .custom-slider-tooltip {
        position: fixed;
        background-color: rgba(31, 41, 55, 0.95);
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 700;
        pointer-events: none;
        white-space: nowrap;
        z-index: 999999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Position the slider container relatively */
    .main [data-baseweb="slider"] {
        position: relative;
    }
    
    /* ============================================= */
    /* Expander/Toggle 설명 박스 스타일 */
    /* ============================================= */
    .stExpander {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    .stExpander > div:first-child {
        background-color: #f1f5f9 !important;
    }
    .stExpander summary {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f1f5f9 !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1e40af !important;
        background-color: white !important;
        border-radius: 6px !important;
    }
    
    /* ============================================= */
    /* 🔥🔥🔥 최종 드롭다운 오버라이드 - !important 전체 적용 */
    /* ============================================= */
    
    /* 드롭다운 리스트 전체 */
    body div[data-baseweb="popover"],
    body div[data-baseweb="menu"],
    body ul[role="listbox"] {
        background: white !important;
        background-color: white !important;
    }
    
    /* 모든 드롭다운 옵션 아이템 */
    body li[role="option"],
    body ul[role="listbox"] > li,
    body div[data-baseweb="menu"] li {
        background: white !important;
        background-color: white !important;
        color: black !important;
    }
    
    /* 옵션 내부 텍스트 강제 */
    body li[role="option"] > div,
    body li[role="option"] span,
    body li[role="option"] div {
        color: black !important;
    }
    
    /* Hover/선택 상태 */
    body li[role="option"]:hover,
    body li[role="option"][aria-selected="true"] {
        background: #e5e7eb !important;
        background-color: #e5e7eb !important;
        color: black !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Create completely custom tooltip overlay
st.markdown("""
    <script>
    (function() {
        let customTooltip = null;
        let activeThumb = null;
        
        function minutesToTime(minutes) {
            const hours = Math.floor(minutes / 60);
            const mins = minutes % 60;
            return String(hours).padStart(2, '0') + ':' + String(mins).padStart(2, '0');
        }
        
        function createTooltip() {
            if (!customTooltip) {
                customTooltip = document.createElement('div');
                customTooltip.className = 'custom-slider-tooltip';
                customTooltip.style.display = 'none';
                document.body.appendChild(customTooltip);
            }
        }
        
        function showTooltip(thumb, event) {
            createTooltip();
            activeThumb = thumb;
            const value = parseInt(thumb.getAttribute('aria-valuenow'));
            
            if (!isNaN(value) && value >= 0 && value <= 1440) {
                customTooltip.textContent = minutesToTime(value);
                customTooltip.style.display = 'block';
                updateTooltipPosition(event || thumb);
            }
        }
        
        function updateTooltipPosition(eventOrElement) {
            if (!customTooltip || customTooltip.style.display === 'none') return;
            
            let x, y;
            if (eventOrElement.clientX !== undefined) {
                // It's an event
                x = eventOrElement.clientX;
                y = eventOrElement.clientY - 45;
            } else {
                // It's an element
                const rect = eventOrElement.getBoundingClientRect();
                x = rect.left + rect.width / 2;
                y = rect.top - 35;
            }
            
            customTooltip.style.left = x + 'px';
            customTooltip.style.top = y + 'px';
            customTooltip.style.transform = 'translateX(-50%)';
        }
        
        function hideTooltip() {
            if (customTooltip) {
                customTooltip.style.display = 'none';
            }
            activeThumb = null;
        }
        
        function attachToSliders() {
            const thumbs = document.querySelectorAll('[role="slider"]');
            
            thumbs.forEach(thumb => {
                if (thumb.dataset.tooltipAttached) return;
                thumb.dataset.tooltipAttached = 'true';
                
                // Mouse events
                thumb.addEventListener('mousedown', (e) => {
                    showTooltip(thumb, e);
                });
                
                thumb.addEventListener('mousemove', (e) => {
                    if (activeThumb === thumb) {
                        const value = parseInt(thumb.getAttribute('aria-valuenow'));
                        if (!isNaN(value)) {
                            customTooltip.textContent = minutesToTime(value);
                        }
                        updateTooltipPosition(e);
                    }
                });
                
                // Touch events
                thumb.addEventListener('touchstart', (e) => {
                    showTooltip(thumb, e.touches[0]);
                });
                
                thumb.addEventListener('touchmove', (e) => {
                    if (activeThumb === thumb && e.touches.length > 0) {
                        const value = parseInt(thumb.getAttribute('aria-valuenow'));
                        if (!isNaN(value)) {
                            customTooltip.textContent = minutesToTime(value);
                        }
                        updateTooltipPosition(e.touches[0]);
                    }
                });
            });
        }
        
        // Global mouse/touch up to hide tooltip
        document.addEventListener('mouseup', hideTooltip);
        document.addEventListener('touchend', hideTooltip);
        
        // Initial attach
        setTimeout(attachToSliders, 300);
        
        // Re-attach on DOM changes
        const observer = new MutationObserver(() => {
            setTimeout(attachToSliders, 100);
        });
        observer.observe(document.body, { childList: true, subtree: true });
        
    })();
    </script>
""", unsafe_allow_html=True)

# Cache data loading functions
@st.cache_data
def load_sward_descriptions():
    """Load S-Ward descriptions and zone information"""
    csv_path = Path('Data/SWard_description/swards.csv')
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path)
    return df

@st.cache_data
def load_position_data(date_str):
    """Load position cache data for a specific date"""
    cache_file = Path('Data/Cache') / f'positions_{date_str}.parquet'
    if not cache_file.exists():
        return None
    return pd.read_parquet(cache_file)

@st.cache_data
def load_stats_data(date_str):
    """Load statistics cache data for a specific date"""
    cache_file = Path('Data/Cache') / f'stats_timeseries_{date_str}.parquet'
    if not cache_file.exists():
        return None
    return pd.read_parquet(cache_file)

@st.cache_data
def load_heatmap_data(date_str):
    """Load heatmap cache data for a specific date"""
    cache_file = Path('Data/Cache') / f'heatmap_cumulative_{date_str}.npz'
    if not cache_file.exists():
        return None
    data = np.load(cache_file)
    return {
        'cumulative_heatmaps': data['cumulative_heatmaps'],
        'time_indices': data['time_indices']
    }

@st.cache_data
def load_map_image():
    """Load base map image"""
    map_path = Path('Data/Map/map_image.png')
    if not map_path.exists():
        # Try alternative name
        map_path = Path('Data/Map/map.png')
        if not map_path.exists():
            return None
    return Image.open(map_path)

def get_available_dates():
    """Get list of available dates from cache files or weather data"""
    # Method 1: Try positions cache (for full functionality)
    cache_dir = Path('Data/Cache')
    if cache_dir.exists():
        position_files = list(cache_dir.glob('positions_*.parquet'))
        if position_files:
            dates = []
            for f in position_files:
                date_str = f.stem.replace('positions_', '')
                # Validate date format (YYYY-MM-DD only, exclude test files)
                if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                    dates.append(date_str)
            return sorted(dates, reverse=True)
    
    # Method 2: Use weather data for date list (for deployment without positions)
    weather_file = Path('Data/Day_description/Day_Weather.csv')
    if weather_file.exists():
        try:
            weather_df = pd.read_csv(weather_file)
            if 'Date' in weather_df.columns:
                dates = weather_df['Date'].tolist()
                return sorted(dates, reverse=True)
        except Exception:
            pass
    
    # Method 3: Fallback - generate date range from model_info
    model_info_file = Path('Data/Cache/Journey/model_info.json')
    if model_info_file.exists():
        try:
            import json
            with open(model_info_file, 'r') as f:
                info = json.load(f)
            training_info = info.get('training_info', {})
            start_date = training_info.get('start_date', '2025-10-01')
            end_date = training_info.get('end_date', '2025-10-21')
            # Generate date list
            from datetime import datetime, timedelta
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            dates = []
            current = start
            while current <= end:
                dates.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
            return sorted(dates, reverse=True)
        except Exception:
            pass
    
    return []

def time_index_to_time(time_index):
    """Convert time_index to HH:MM format"""
    seconds = (time_index - 1) * 10
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def time_to_time_index(time_str):
    """Convert HH:MM to time_index"""
    hours, minutes = map(int, time_str.split(':'))
    seconds = hours * 3600 + minutes * 60
    return (seconds // 10) + 1

def create_zone_mapping(sward_df):
    """Create mapping from S-Ward to Zone"""
    zone_mapping = {}
    zone_swards = {}
    
    for _, row in sward_df.iterrows():
        sward = row['name']
        zone = row['description']
        zone_mapping[sward] = zone
        
        if zone not in zone_swards:
            zone_swards[zone] = []
        zone_swards[zone].append(sward)
    
    return zone_mapping, zone_swards

# =====================================================
# SIDEBAR
# =====================================================

def render_sidebar():
    """Render sidebar with date selection and main menu"""
    with st.sidebar:
        st.title("🏪 DeepCommerce")
        st.markdown("<p style='color: #9ca3af; font-size: 14px; margin-top: -10px;'>Sector : Retail store</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Date Selection
        st.subheader("📅 Select Date")
        available_dates = get_available_dates()
        
        if not available_dates:
            st.error("No data available")
            return None, None
        
        selected_date = st.selectbox(
            "Date",
            available_dates,
            format_func=lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%B %d, %Y'),
            label_visibility="collapsed"
        )
        
        # Date Info
        if selected_date:
            st.markdown("---")
            st.subheader("📊 Date Info")
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            st.info(f"""
            **Date:** {date_obj.strftime('%B %d, %Y')}  
            **Day:** {date_obj.strftime('%A')}  
            **Week:** Week {date_obj.isocalendar()[1]}
            """)
        
        # Main Menu
        st.markdown("---")
        st.subheader("📋 Main Menu")
        
        menu_options = [
            "🚶 Traffic Analysis",
            "📍 Localization",
            "🔥 Heatmap Analysis",
            "🌐 Spatial Flow",
            "🔮 Flow Prediction"
        ]
        
        selected_menu = st.radio(
            "Navigation",
            menu_options,
            label_visibility="collapsed"
        )
        
        return selected_date, selected_menu

# =====================================================
# TRAFFIC ANALYSIS
# =====================================================

def render_traffic_analysis(date_str):
    """Render traffic analysis page"""
    st.title("🚶 Traffic Analysis")
    st.markdown(f"<p style='color: #4b5563;'><strong>Date:</strong> {datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    stats_df = load_stats_data(date_str)
    positions_df = load_position_data(date_str)
    sward_df = load_sward_descriptions()
    
    if stats_df is None or positions_df is None or sward_df is None:
        st.error("Data not available for selected date")
        return
    
    # Create zone mapping
    zone_mapping, zone_swards = create_zone_mapping(sward_df)
    
    # Add zone to positions
    positions_df['zone'] = positions_df['sward_name'].map(zone_mapping)
    
    # Section 1: Total Traffic
    st.header("1️⃣ Total Traffic Over Time")
    
    # Aggregate by time (1-minute intervals)
    total_traffic = stats_df.groupby('time_index')['total_devices'].first().reset_index()
    total_traffic['time'] = total_traffic['time_index'].apply(time_index_to_time)
    total_traffic['hour_decimal'] = total_traffic['time_index'].apply(lambda x: ((x-1) * 10) / 3600)
    
    fig_total = go.Figure()
    fig_total.add_trace(go.Scatter(
        x=total_traffic['hour_decimal'],
        y=total_traffic['total_devices'],
        mode='lines',
        name='Total Devices',
        line=dict(color='#3b82f6', width=2),
        hovertemplate='<b>Time:</b> %{text}<br><b>Devices:</b> %{y}<extra></extra>',
        text=total_traffic['time']
    ))
    
    fig_total.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Number of Devices",
        xaxis=dict(range=[0, 24], dtick=1),
        yaxis=dict(dtick=10),
        template="plotly_white",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_total, use_container_width=True)
    
    # Section 2: Zone Traffic
    st.header("2️⃣ Zone-Specific Traffic")
    
    zones = sorted(list(zone_swards.keys()), key=str.lower)
    
    # Find Self checkout as default
    checkout_zones = [z for z in zones if 'self checkout' in z.lower()]
    default_zone = checkout_zones[0] if checkout_zones else (zones[0] if zones else None)
    
    selected_zones = st.multiselect(
        "Select zones to compare:",
        zones,
        default=[default_zone] if default_zone else []
    )
    
    if selected_zones:
        # Calculate zone traffic (1-minute intervals)
        zone_traffic_data = []
        
        for zone in selected_zones:
            swards_in_zone = zone_swards[zone]
            zone_stats = stats_df[stats_df['sward_name'].isin(swards_in_zone)]
            zone_traffic = zone_stats.groupby('time_index')['count'].sum().reset_index()
            zone_traffic['zone'] = zone
            zone_traffic['hour_decimal'] = zone_traffic['time_index'].apply(lambda x: ((x-1) * 10) / 3600)
            zone_traffic['time'] = zone_traffic['time_index'].apply(time_index_to_time)
            zone_traffic_data.append(zone_traffic)
        
        if zone_traffic_data:
            combined_zone_traffic = pd.concat(zone_traffic_data)
            
            fig_zones = go.Figure()
            
            for zone in selected_zones:
                zone_data = combined_zone_traffic[combined_zone_traffic['zone'] == zone]
                fig_zones.add_trace(go.Scatter(
                    x=zone_data['hour_decimal'],
                    y=zone_data['count'],
                    mode='lines',
                    name=zone,
                    line=dict(width=2),
                    hovertemplate='<b>Time:</b> %{text}<br><b>Devices:</b> %{y}<extra></extra>',
                    text=zone_data['time']
                ))
            
            fig_zones.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Number of Devices",
                xaxis=dict(range=[0, 24], dtick=1),
                template="plotly_white",
                height=400,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_zones, use_container_width=True)
    
    # Section 3: Cumulative Visitors
    st.header("3️⃣ Cumulative Visitor Count")
    
    # Zone selection
    checkout_zones = [z for z in zones if 'self checkout' in z.lower()]
    default_zone_cum = checkout_zones[0] if checkout_zones else (zones[0] if zones else None)
    
    selected_zones_cum = st.multiselect(
        "Select zones:",
        zones,
        default=[default_zone_cum] if default_zone_cum else []
    )
    
    # Dwell time selection
    dwell_time = st.radio(
        "Minimum dwell time (minutes):",
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=0
    )
    
    # Calculate cumulative visitors for selected zones
    if not selected_zones_cum:
        st.warning("Please select at least one zone")
        return
    
    zone_positions = positions_df[positions_df['zone'].isin(selected_zones_cum)].copy()
    
    if len(zone_positions) == 0:
        st.warning(f"No data found for zones: {selected_zones_cum}")
        cumulative_hourly = pd.DataFrame({'hour': range(24), 'cumulative_visitors': [0] * 24})
    else:
        # Group by MAC and calculate dwell time
        mac_dwell = zone_positions.groupby('mac_address').agg({
            'time_index': ['min', 'max', 'count']
        }).reset_index()
        mac_dwell.columns = ['mac_address', 'first_seen', 'last_seen', 'count']
        mac_dwell['dwell_minutes'] = (mac_dwell['last_seen'] - mac_dwell['first_seen']) * 10 / 60
        
        # Filter by dwell time
        qualified_macs = mac_dwell[mac_dwell['dwell_minutes'] >= dwell_time]['mac_address'].unique()
        
        if len(qualified_macs) == 0:
            cumulative_hourly = pd.DataFrame({'hour': range(24), 'cumulative_visitors': [0] * 24})
        else:
            # Calculate cumulative count over time
            cumulative_data = []
            seen_macs = set()
            
            for time_idx in sorted(zone_positions['time_index'].unique()):
                # Get MACs at this time
                current_macs = set(zone_positions[zone_positions['time_index'] == time_idx]['mac_address'].unique())
                # Add to seen set
                seen_macs.update(current_macs)
                # Count qualified MACs
                qualified_count = len(seen_macs & set(qualified_macs))
                hour_decimal = ((time_idx - 1) * 10) / 3600
                time_str = time_index_to_time(time_idx)
                cumulative_data.append({'time_index': time_idx, 'hour_decimal': hour_decimal, 'time': time_str, 'cumulative_visitors': qualified_count})
            
            cumulative_df = pd.DataFrame(cumulative_data)
    
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(
        x=cumulative_df['hour_decimal'],
        y=cumulative_df['cumulative_visitors'],
        mode='lines',
        name='Cumulative Visitors',
        line=dict(color='#10b981', width=2),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)',
        hovertemplate='<b>Time:</b> %{text}<br><b>Visitors:</b> %{y}<extra></extra>',
        text=cumulative_df['time']
    ))
    
    fig_cum.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Cumulative Visitors",
        xaxis=dict(range=[0, 24], dtick=1),
        template="plotly_white",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_cum, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        if len(zone_positions) > 0 and len(qualified_macs) > 0:
            st.metric("Total Qualified Visitors", len(qualified_macs))
        else:
            st.metric("Total Qualified Visitors", 0)
    with col2:
        if len(zone_positions) > 0 and len(qualified_macs) > 0:
            avg_dwell = mac_dwell[mac_dwell['mac_address'].isin(qualified_macs)]['dwell_minutes'].mean()
            st.metric("Avg Dwell Time", f"{avg_dwell:.1f} min")
        else:
            st.metric("Avg Dwell Time", "0.0 min")
    with col3:
        st.metric("Selected Zones", f"{len(selected_zones_cum)} zones")

# =====================================================
# LOCALIZATION
# =====================================================

def render_localization(date_str):
    """Render localization page with video playback"""
    st.title("📍 Localization")
    st.markdown(f"<p style='color: #4b5563;'><strong>Date:</strong> {datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load position data
    positions_df = load_position_data(date_str)
    if positions_df is None:
        st.error("No position data available for this date")
        return
    
    # Load map
    map_img = load_map_image()
    if map_img is None:
        st.warning("Map image not found")
        map_img = Image.new('RGB', (696, 509), color='white')
    
    # Time selection using sliders
    st.subheader("⏰ Time Range")
    
    # Convert time to minutes since midnight
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 5px;'>Start Time</p>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; color: #6b7280; font-size: 12px; margin-bottom: -10px;'><span>00:00</span><span>24:00</span></div>", unsafe_allow_html=True)
        start_minutes = st.slider(
            "start_time_label",
            min_value=0,
            max_value=1440,
            value=540,  # 09:00
            step=10,
            label_visibility="collapsed",
            key="loc_start_slider"
        )
        start_hour = start_minutes // 60
        start_minute = start_minutes % 60
        st.markdown(f"<h2 style='text-align: center; color: #1f2937; margin-top: 5px;'>⏰ {start_hour:02d}:{start_minute:02d}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 5px;'>End Time</p>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; color: #6b7280; font-size: 12px; margin-bottom: -10px;'><span>00:00</span><span>24:00</span></div>", unsafe_allow_html=True)
        end_minutes = st.slider(
            "end_time_label",
            min_value=0,
            max_value=1440,
            value=600,  # 10:00
            step=10,
            label_visibility="collapsed",
            key="loc_end_slider"
        )
        end_hour = end_minutes // 60
        end_minute = end_minutes % 60
        st.markdown(f"<h2 style='text-align: center; color: #1f2937; margin-top: 5px;'>⏰ {end_hour:02d}:{end_minute:02d}</h2>", unsafe_allow_html=True)
    
    start_time_idx = (start_hour * 3600 + start_minute * 60) // 10 + 1
    end_time_idx = (end_hour * 3600 + end_minute * 60) // 10 + 1
    
    if start_time_idx >= end_time_idx:
        st.error("End time must be after start time")
        return
    
    # Playback controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        play_button = st.button("▶️ Play", key="loc_play")
    with col2:
        pause_button = st.button("⏸️ Pause", key="loc_pause")
    with col3:
        reset_button = st.button("🔄 Reset", key="loc_reset")
    with col4:
        speed = st.select_slider("Speed", options=["0.5x", "1x", "2x", "4x", "8x", "16x"], value="2x", key="loc_speed")
    
    # Initialize session state
    if 'loc_playing' not in st.session_state:
        st.session_state.loc_playing = False
        st.session_state.loc_current_idx = 0
    
    if play_button:
        st.session_state.loc_playing = True
    if pause_button:
        st.session_state.loc_playing = False
    if reset_button:
        st.session_state.loc_current_idx = 0
        st.session_state.loc_playing = False
    
    # Filter data by time range
    filtered_positions = positions_df[(positions_df['time_index'] >= start_time_idx) & 
                                     (positions_df['time_index'] <= end_time_idx)].copy()
    
    if len(filtered_positions) == 0:
        st.warning("No position data in selected time range")
        return
    
    # Get unique time indices
    time_indices = sorted(filtered_positions['time_index'].unique())
    
    # Speed mapping
    speed_map = {"0.5x": 0.5, "1x": 1, "2x": 2, "4x": 4, "8x": 8, "16x": 16}
    frame_skip = int(speed_map[speed])
    
    # Auto-play logic
    if st.session_state.loc_playing:
        st.session_state.loc_current_idx += frame_skip
        if st.session_state.loc_current_idx >= len(time_indices):
            st.session_state.loc_current_idx = len(time_indices) - 1
            st.session_state.loc_playing = False
    
    current_time_idx = time_indices[min(st.session_state.loc_current_idx, len(time_indices) - 1)]
    current_positions = filtered_positions[filtered_positions['time_index'] == current_time_idx]
    
    # Count devices by type
    ios_count = len(current_positions[current_positions['mac_address'].str.startswith(('02:', '06:', '0A:', '0E:'))])
    android_count = len(current_positions) - ios_count
    total_count = len(current_positions)
    
    # Create visualization
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=80)
    ax.imshow(map_img)
    
    # Plot positions - separate iOS and Android
    if len(current_positions) > 0:
        ios_positions = current_positions[current_positions['mac_address'].str.startswith(('02:', '06:', '0A:', '0E:'))]
        android_positions = current_positions[~current_positions['mac_address'].str.startswith(('02:', '06:', '0A:', '0E:'))]
        
        if len(ios_positions) > 0:
            ax.scatter(ios_positions['x'], ios_positions['y'], 
                      c='#3b82f6', s=50, alpha=0.7, edgecolors='white', linewidths=1, label='iOS')
        if len(android_positions) > 0:
            ax.scatter(android_positions['x'], android_positions['y'], 
                      c='#ef4444', s=50, alpha=0.7, edgecolors='white', linewidths=1, label='Android')
    
    # Add time text (top-left)
    current_time_str = time_index_to_time(current_time_idx)
    ax.text(10, 30, current_time_str, fontsize=24, color='white', 
           bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), weight='bold')
    
    # Add device count (top-right)
    count_text = f"iOS {ios_count} / Android {android_count} / Total {total_count}"
    ax.text(686, 30, count_text, fontsize=18, color='white', ha='right',
           bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), weight='bold')
    
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    # Convert to image buffer to prevent flickering
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close(fig)
    
    # Display using st.image (no flickering)
    st.image(buf, use_container_width=True)
    
    # Progress bar
    progress = st.session_state.loc_current_idx / max(len(time_indices) - 1, 1)
    st.progress(progress)
    st.caption(f"Frame {st.session_state.loc_current_idx + 1} / {len(time_indices)}")
    
    # Auto-refresh if playing
    if st.session_state.loc_playing:
        import time
        time.sleep(0.1)
        st.rerun()

# =====================================================
# HEATMAP ANALYSIS
# =====================================================

def render_heatmap_analysis(date_str):
    """Render heatmap analysis page"""
    st.title("🔥 Heatmap Analysis")
    st.markdown(f"<p style='color: #4b5563;'><strong>Date:</strong> {datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Only static image mode for deployment (video mode removed to save 7GB)
    render_heatmap_static(date_str)


def render_heatmap_static(date_str):
    """Render static heatmap images (lightweight for deployment)"""
    st.markdown("---")
    
    # Check for pre-generated heatmap images
    heatmap_image_dir = Path('Data/Cache/Heatmap')
    
    # Time period selection
    st.subheader("⏰ Time Period")
    time_period = st.selectbox(
        "Select time period",
        ["Full Day (06:00 - 22:00)", "Morning (06:00 - 12:00)", "Afternoon (12:00 - 18:00)", "Evening (18:00 - 22:00)"],
        label_visibility="collapsed"
    )
    
    period_map = {
        "Full Day (06:00 - 22:00)": "full",
        "Morning (06:00 - 12:00)": "morning",
        "Afternoon (12:00 - 18:00)": "afternoon",
        "Evening (18:00 - 22:00)": "evening"
    }
    period_key = period_map[time_period]
    
    # Look for cached heatmap image
    image_path = heatmap_image_dir / f"heatmap_{date_str}_{period_key}.png"
    
    if image_path.exists():
        # Load and display cached image
        st.image(str(image_path), use_container_width=True)
        st.success(f"✅ Showing cumulative heatmap for {time_period}")
    else:
        # Generate heatmap on-the-fly (fallback)
        st.info("⏳ Generating heatmap... This may take a moment.")
        heatmap_data = load_heatmap_data(date_str)
        
        if heatmap_data is None:
            st.warning("⚠️ No heatmap data available for this date.")
            st.info("💡 **Note:** Heatmap data requires the full cache files which are not included in the web deployment version due to storage limitations (~7GB). Please use the local version for full heatmap functionality.")
            return
        
        cumulative_heatmaps = heatmap_data['cumulative_heatmaps']
        time_indices = heatmap_data['time_indices']
        
        # Define time ranges
        time_ranges = {
            "full": (2160, 7920),      # 06:00 - 22:00
            "morning": (2160, 4320),   # 06:00 - 12:00
            "afternoon": (4320, 6480), # 12:00 - 18:00
            "evening": (6480, 7920)    # 18:00 - 22:00
        }
        start_idx, end_idx = time_ranges[period_key]
        
        # Find the heatmap at end time
        target_idx = None
        for i, t in enumerate(time_indices):
            if t <= end_idx:
                target_idx = i
            else:
                break
        
        baseline_idx = None
        for i, t in enumerate(time_indices):
            if t <= start_idx:
                baseline_idx = i
            else:
                break
        
        if target_idx is None:
            st.error("No data in selected time range")
            return
        
        # Calculate difference
        if baseline_idx is not None and baseline_idx < len(cumulative_heatmaps):
            heatmap_diff = cumulative_heatmaps[target_idx].astype(float) - cumulative_heatmaps[baseline_idx].astype(float)
            heatmap_diff[heatmap_diff < 0] = 0
        else:
            heatmap_diff = cumulative_heatmaps[target_idx].astype(float)
        
        # Create visualization
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
        from scipy.ndimage import gaussian_filter
        
        map_img = load_map_image()
        if map_img is None:
            map_img = Image.new('RGB', (696, 509), color='white')
        
        fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
        ax.imshow(map_img)
        
        colors = ['#00000000', '#ffff00ff', '#ff8c00ff', '#ff0000ff', '#8b0000ff']
        cmap = LinearSegmentedColormap.from_list('custom_heat', colors, N=256)
        
        heatmap_display = gaussian_filter(heatmap_diff, sigma=2.0)
        max_val = np.max(heatmap_display)
        if max_val > 0:
            heatmap_display = np.sqrt(heatmap_display / max_val) * max_val
        heatmap_display[heatmap_display == 0] = np.nan
        
        ax.imshow(heatmap_display, cmap=cmap, alpha=0.8, vmin=0, vmax=np.nanmax(cumulative_heatmaps[target_idx]) if np.nanmax(cumulative_heatmaps[target_idx]) > 0 else 1)
        
        # Add title
        period_times = {
            "full": "06:00 - 22:00",
            "morning": "06:00 - 12:00",
            "afternoon": "12:00 - 18:00",
            "evening": "18:00 - 22:00"
        }
        ax.text(10, 30, f"{time_period.split('(')[0].strip()}: {period_times[period_key]}", 
               fontsize=18, color='white', 
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), weight='bold')
        
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        plt.close(fig)
        
        st.image(buf, use_container_width=True)
    
    # Stats section
    st.markdown("---")
    st.subheader("📊 Heatmap Interpretation")
    
    with st.expander("ℹ️ How to read the heatmap", expanded=False):
        st.markdown("""
        **Color Scale:**
        - 🟡 **Yellow** = Low activity
        - 🟠 **Orange** = Medium activity
        - 🔴 **Red** = High activity
        - 🟤 **Dark Red** = Very high activity (hotspot)
        
        **Key Insights:**
        - Hotspots indicate areas where visitors spend the most time
        - Use this to optimize product placement and store layout
        - Compare different time periods to understand traffic patterns
        """)


def render_heatmap_video(date_str):
    """Render animated heatmap video (requires full cache data)"""
    st.markdown("---")
    
    # Check if full heatmap data is available
    heatmap_data = load_heatmap_data(date_str)
    
    if heatmap_data is None:
        st.warning("⚠️ **Animated Video not available in web deployment**")
        st.info("""
        📦 **Storage Limitation**
        
        The animated heatmap feature requires the full heatmap cache files (~7GB for 21 days), 
        which exceeds Streamlit Cloud's free tier storage limits.
        
        **Options:**
        1. Use **Static Image** mode (recommended for web)
        2. Run the dashboard locally with full cache data
        3. Contact admin for enterprise deployment with full features
        
        💡 **Tip:** Static images provide the same insights with much faster loading!
        """)
        return
    
    # Original video playback code
    cumulative_heatmaps = heatmap_data['cumulative_heatmaps']
    time_indices = heatmap_data['time_indices']
    
    # Load map
    map_img = load_map_image()
    if map_img is None:
        st.warning("Map image not found")
        map_img = Image.new('RGB', (696, 509), color='white')
    
    # Time selection using sliders
    st.subheader("⏰ Time Range")
    
    # Convert time to minutes since midnight
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 5px;'>Start Time</p>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; color: #6b7280; font-size: 12px; margin-bottom: -10px;'><span>00:00</span><span>24:00</span></div>", unsafe_allow_html=True)
        start_minutes = st.slider(
            "start_time_label",
            min_value=0,
            max_value=1440,
            value=540,  # 09:00
            step=10,
            label_visibility="collapsed",
            key="hm_start_slider"
        )
        start_hour = start_minutes // 60
        start_minute = start_minutes % 60
        st.markdown(f"<h2 style='text-align: center; color: #1f2937; margin-top: 5px;'>⏰ {start_hour:02d}:{start_minute:02d}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 5px;'>End Time</p>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; color: #6b7280; font-size: 12px; margin-bottom: -10px;'><span>00:00</span><span>24:00</span></div>", unsafe_allow_html=True)
        end_minutes = st.slider(
            "end_time_label",
            min_value=0,
            max_value=1440,
            value=600,  # 10:00
            step=10,
            label_visibility="collapsed",
            key="hm_end_slider"
        )
        end_hour = end_minutes // 60
        end_minute = end_minutes % 60
        st.markdown(f"<h2 style='text-align: center; color: #1f2937; margin-top: 5px;'>⏰ {end_hour:02d}:{end_minute:02d}</h2>", unsafe_allow_html=True)
    
    start_time_idx = (start_hour * 3600 + start_minute * 60) // 10 + 1
    end_time_idx = (end_hour * 3600 + end_minute * 60) // 10 + 1
    
    if start_time_idx >= end_time_idx:
        st.error("End time must be after start time")
        return
    
    # Playback controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        play_button = st.button("▶️ Play", key="hm_play")
    with col2:
        pause_button = st.button("⏸️ Pause", key="hm_pause")
    with col3:
        reset_button = st.button("🔄 Reset", key="hm_reset")
    with col4:
        speed = st.select_slider("Speed", options=["0.5x", "1x", "2x", "4x", "8x", "16x"], value="2x", key="hm_speed")
    
    # Initialize session state
    if 'hm_playing' not in st.session_state:
        st.session_state.hm_playing = False
        st.session_state.hm_current_idx = 0
    
    if play_button:
        st.session_state.hm_playing = True
    if pause_button:
        st.session_state.hm_playing = False
    if reset_button:
        st.session_state.hm_current_idx = 0
        st.session_state.hm_playing = False
    
    # Filter time indices
    valid_indices = [(i, t) for i, t in enumerate(time_indices) if start_time_idx <= t <= end_time_idx]
    
    if len(valid_indices) == 0:
        st.warning("No heatmap data in selected time range")
        return
    
    # Speed mapping
    speed_map = {"0.5x": 1, "1x": 2, "2x": 4, "4x": 8, "8x": 16, "16x": 32}
    frame_skip = speed_map[speed]
    
    # Auto-play logic
    if st.session_state.hm_playing:
        st.session_state.hm_current_idx += frame_skip
        if st.session_state.hm_current_idx >= len(valid_indices):
            st.session_state.hm_current_idx = len(valid_indices) - 1
            st.session_state.hm_playing = False
    
    current_frame_idx = min(st.session_state.hm_current_idx, len(valid_indices) - 1)
    heatmap_idx, current_time_idx = valid_indices[current_frame_idx]
    current_heatmap = cumulative_heatmaps[heatmap_idx]
    
    # Find baseline heatmap (just before start time)
    baseline_idx = None
    baseline_time_idx = start_time_idx - 1
    for i, t in enumerate(time_indices):
        if t <= baseline_time_idx:
            baseline_idx = i
        else:
            break
    
    # Calculate difference from baseline
    if baseline_idx is not None and baseline_idx < len(cumulative_heatmaps):
        baseline_heatmap = cumulative_heatmaps[baseline_idx]
        heatmap_diff = current_heatmap.astype(float) - baseline_heatmap.astype(float)
        heatmap_diff[heatmap_diff < 0] = 0  # Remove negative values
    else:
        heatmap_diff = current_heatmap.astype(float)
    
    # Create visualization
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from scipy.ndimage import gaussian_filter
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=80)
    ax.imshow(map_img)
    
    # Create custom colormap (더 강한 색상)
    colors = ['#00000000', '#ffff00ff', '#ff8c00ff', '#ff0000ff', '#8b0000ff']
    n_bins = 256
    cmap = LinearSegmentedColormap.from_list('custom_heat', colors, N=n_bins)
    
    # Apply Gaussian smoothing for better visualization
    heatmap_display = gaussian_filter(heatmap_diff, sigma=2.0)
    
    # Normalize with square root for better visibility
    max_val = np.max(heatmap_display)
    if max_val > 0:
        heatmap_display = np.sqrt(heatmap_display / max_val) * max_val
    
    heatmap_display[heatmap_display == 0] = np.nan  # Make zeros transparent
    
    # Higher alpha for stronger visibility
    im = ax.imshow(heatmap_display, cmap=cmap, alpha=0.8, vmin=0, vmax=np.nanmax(current_heatmap) if np.nanmax(current_heatmap) > 0 else 1)
    
    # Add time text (top-left)
    current_time_str = time_index_to_time(current_time_idx)
    ax.text(10, 30, current_time_str, fontsize=24, color='white', 
           bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), weight='bold')
    
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    # Convert to image buffer to prevent flickering
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close(fig)
    
    # Display using st.image (no flickering)
    st.image(buf, use_container_width=True)
    
    # Progress bar
    progress = st.session_state.hm_current_idx / max(len(valid_indices) - 1, 1)
    st.progress(progress)
    st.caption(f"Frame {st.session_state.hm_current_idx + 1} / {len(valid_indices)}")
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Intensity", int(np.nanmax(heatmap_display) if not np.all(np.isnan(heatmap_display)) else 0))
    with col2:
        st.metric("Mean Intensity", f"{np.nanmean(heatmap_display):.1f}" if not np.all(np.isnan(heatmap_display)) else "0")
    with col3:
        st.metric("Active Pixels", int(np.sum(~np.isnan(heatmap_display))))
    
    # Auto-refresh if playing
    if st.session_state.hm_playing:
        import time
        time.sleep(0.1)
        st.rerun()

# =====================================================
# JOURNEY ANALYSIS (Cache-based Spatial Flow)
# =====================================================

# Import cache loader
from src.journey_cache_loader import (
    load_zone_transitions,
    load_zone_statistics,
    load_journey_predictions,
    load_comparative_analysis,
    get_filtered_transitions,
    get_filtered_transitions_with_fallback,
    get_zone_outflow_probabilities,
    get_zone_inflow_sources,
    get_zone_outflow_with_fallback,
    get_zone_inflow_with_fallback,
    check_cache_status
)

def render_journey_analysis(date_str):
    """Render Spatial Flow Analysis - Cache-based fast loading with detailed explanations"""
    st.title("🌐 Spatial Flow Analysis")
    st.markdown("---")
    
    # Load cached data (instant!)
    transitions_df = load_zone_transitions()
    zone_stats = load_zone_statistics()
    comp_df = load_comparative_analysis()
    sward_df = load_sward_descriptions()
    
    if transitions_df is None:
        st.error("❌ Cache not found. Run `python precompute_journey_cache.py` first.")
        return
    
    # Philosophy explanation with toggle
    with st.expander("💡 What is Space-Centric Spatial AI?", expanded=False):
        st.markdown("""
        ### Space-Centric Approach
        
        **Flow Analytics learns "Spatial Grammar"** - the statistical patterns of movement through space.
        
        | Traditional Approach | Space-Centric Approach |
        |---------------------|------------------------|
        | Track individuals | Learn movement patterns |
        | Requires persistent ID | Works with MAC randomization |
        | Privacy concerns | Privacy-preserving |
        | "Person A went here" | "35% of visitors go here" |
        
        **Key Concepts:**
        - **Micro-Trajectory**: 5-10 minute observation windows as reliable data units
        - **Population-Level**: Aggregate flow probabilities, not individual tracking
        - **Zone-to-Zone Transitions**: Adjacent zones only (physically possible movements)
        - **Spatial Grammar**: Statistical patterns that repeat across time
        
        **Why Adjacent Zones Only?**
        - Visitors physically cannot teleport between non-adjacent zones
        - Only transitions between neighboring zones are counted
        - This ensures data integrity and realistic movement patterns
        """)
    
    st.markdown("---")
    
    # Filter controls with explanation
    st.subheader("🔧 Filter Options")
    
    with st.expander("ℹ️ How do filters work?", expanded=False):
        st.markdown("""
        **Filters allow you to analyze flow patterns under specific conditions:**
        - **Weekday**: Movement patterns differ between weekdays and weekends
        - **Weather**: Rainy days may change shopping behavior
        - **Time Period**: Morning, afternoon, and evening have distinct patterns
        
        Combining filters reveals contextual insights like:
        *"On rainy Saturday afternoons, 40% more visitors go to the Food Court"*
        """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        selected_weekday = st.selectbox("Weekday", ['All'] + weekday_names, key="sf_weekday")
        weekday_filter = weekday_names.index(selected_weekday) if selected_weekday != 'All' else None
    
    with col2:
        weather_options = ['All', 'Clear', 'Rainy', 'Cloudy']
        selected_weather = st.selectbox("Weather", weather_options, key="sf_weather")
        weather_filter = selected_weather if selected_weather != 'All' else None
    
    with col3:
        time_options = ['All', 'morning', 'afternoon', 'evening']
        time_labels = ['All', 'Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-22)']
        selected_time = st.selectbox("Time Period", time_labels, key="sf_time")
        time_filter = time_options[time_labels.index(selected_time)] if selected_time != 'All' else None
    
    # Filter transitions with fallback support
    filtered_trans, fallback_msg = get_filtered_transitions_with_fallback(
        transitions_df, weekday_filter, weather_filter, time_filter
    )
    
    # Display fallback message if applicable
    if fallback_msg:
        st.info(fallback_msg)
    
    # Remove same-zone transitions (should already be filtered in cache, but double-check)
    if len(filtered_trans) > 0:
        filtered_trans = filtered_trans[filtered_trans['from_zone'] != filtered_trans['to_zone']]
    
    if len(filtered_trans) == 0:
        st.warning("⚠️ No data for selected filters. Try 'All' for broader results.")
        return
    
    st.markdown("---")
    
    # Summary metrics
    total_transitions = filtered_trans['count'].sum()
    unique_flows = len(filtered_trans.groupby(['from_zone', 'to_zone']))
    unique_zones = len(set(filtered_trans['from_zone'].unique()) | set(filtered_trans['to_zone'].unique()))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transitions", f"{total_transitions:,}")
    with col2:
        st.metric("Unique Zone-to-Zone Flows", f"{unique_flows:,}")
    with col3:
        st.metric("Active Zones", f"{unique_zones}")
    
    st.markdown("---")
    
    # Section 1: Top Flow Patterns
    st.subheader("🎯 Zone-to-Zone Transitions")
    
    with st.expander("ℹ️ About Zone Transitions", expanded=False):
        st.markdown("""
        **Zone-to-Zone Transitions** show how visitors move between adjacent zones.
        
        - Only **adjacent zones** are included (physically possible movements)
        - Same-zone transitions are excluded
        - Higher count = more popular route
        - Use this to identify **main traffic corridors**
        
        **AI Interpretation Tips:**
        - High-traffic corridors are ideal for advertising placement
        - Unexpected low-traffic routes may indicate navigation issues
        - Compare weekday vs weekend patterns for operational insights
        """)
    
    # Filter options
    col_filter1, col_filter2 = st.columns([1, 3])
    with col_filter1:
        exclude_entrance = st.checkbox("🚪 Exclude Entrance-related flows", value=False,
                                       help="Filter out transitions to/from Entrance zone (often noisy due to ward placement)")
    
    # Aggregate by from_zone, to_zone
    flow_agg = filtered_trans.groupby(['from_zone', 'to_zone'])['count'].sum().reset_index()
    
    # Apply entrance filter if selected
    if exclude_entrance:
        flow_agg = flow_agg[
            (~flow_agg['from_zone'].str.lower().str.contains('entrance')) & 
            (~flow_agg['to_zone'].str.lower().str.contains('entrance'))
        ]
    
    flow_agg = flow_agg.sort_values('count', ascending=False)
    
    # Top 15 flows
    top_flows = flow_agg.head(15).copy()
    top_flows['flow'] = top_flows['from_zone'] + ' → ' + top_flows['to_zone']
    
    fig_flows = go.Figure()
    fig_flows.add_trace(go.Bar(
        y=top_flows['flow'],
        x=top_flows['count'],
        orientation='h',
        marker_color='#10b981',
        text=top_flows['count'],
        textposition='auto'
    ))
    fig_flows.update_layout(
        title="Top 15 Zone Transitions",
        xaxis_title="Frequency",
        yaxis_title="",
        template="plotly_white",
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig_flows, use_container_width=True)
    
    st.info(f"📊 Total Transitions: **{flow_agg['count'].sum():,}** | Unique Flows: **{len(flow_agg):,}**")
    
    st.markdown("---")
    
    # Section 2: Dwell Time Analysis (NEW!)
    st.subheader("⏱️ Zone Dwell Time Ranking")
    
    with st.expander("ℹ️ About Dwell Time Analysis", expanded=False):
        st.markdown("""
        **Dwell Time** measures how long visitors stay in each zone.
        
        - **High dwell time** = Strong engagement (e.g., browsing, trying products)
        - **Low dwell time** = Pass-through zone or quick pick-up area
        
        **Strategic Insights:**
        - High-dwell zones are ideal for product placement
        - Low-dwell zones may need better attractions
        - Compare with zone purpose (e.g., entrance should have low dwell)
        """)
    
    if zone_stats:
        # Create dwell time ranking
        dwell_data = []
        for zone, stats in zone_stats.items():
            avg_dwell = stats.get('avg_dwell_time', 0)
            rank = stats.get('dwell_time_rank', 99)
            total_visitors = stats.get('total_visitors', 0)
            if avg_dwell > 0:
                dwell_data.append({
                    'Zone': zone,
                    'Avg Dwell (min)': round(avg_dwell, 1),
                    'Rank': rank,
                    'Visitors': total_visitors
                })
        
        if dwell_data:
            dwell_df = pd.DataFrame(dwell_data).sort_values('Avg Dwell (min)', ascending=False).head(15)
            
            fig_dwell = go.Figure()
            fig_dwell.add_trace(go.Bar(
                y=dwell_df['Zone'],
                x=dwell_df['Avg Dwell (min)'],
                orientation='h',
                marker_color='#8b5cf6',
                text=[f"{d:.1f} min" for d in dwell_df['Avg Dwell (min)']],
                textposition='auto'
            ))
            fig_dwell.update_layout(
                title="Top 15 Zones by Average Dwell Time",
                xaxis_title="Average Dwell Time (minutes)",
                yaxis_title="",
                template="plotly_white",
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig_dwell, use_container_width=True)
            
            # AI Interpretation for Dwell Time
            if len(dwell_df) > 0:
                top_dwell_zone = dwell_df.iloc[0]['Zone']
                top_dwell_time = dwell_df.iloc[0]['Avg Dwell (min)']
                st.success(f"""
                🤖 **AI Insight**: The **{top_dwell_zone}** zone has the highest dwell time ({top_dwell_time:.1f} min). 
                This indicates strong visitor engagement. Consider this zone for:
                - Premium product placement
                - Interactive displays
                - Promotional activities
                """)
    
    st.markdown("---")
    
    # Section 3: Zone Traffic Summary (Improved)
    st.subheader("🏪 Zone Traffic Summary")
    
    with st.expander("ℹ️ About Inflow/Outflow", expanded=False):
        st.markdown("""
        **Inflow vs Outflow** shows the directional traffic for each zone.
        
        - **Inflow** = Transitions coming INTO the zone from adjacent zones
        - **Outflow** = Transitions going OUT from the zone to adjacent zones
        
        **Why are they similar?**
        - For most zones, inflow ≈ outflow (visitors enter and exit)
        - Differences indicate zone function:
          - **Entrance**: Higher outflow (starting point)
          - **Exit/Checkout**: Higher inflow (ending point)
          - **Dead-end zones**: Lower outflow
        
        **Strategic Use:**
        - High-traffic zones = prime advertising locations
        - Asymmetric zones = understand customer flow direction
        """)
    
    if zone_stats:
        # Create zone traffic dataframe with more metrics
        zone_traffic = []
        for zone, stats in zone_stats.items():
            outflow = stats.get('total_outflow', 0)
            inflow = stats.get('total_inflow', 0)
            zone_traffic.append({
                'Zone': zone,
                'Outflow': outflow,
                'Inflow': inflow,
                'Total': outflow + inflow,
                'Balance': outflow - inflow  # Positive = source, Negative = sink
            })
        
        zone_traffic_df = pd.DataFrame(zone_traffic).sort_values('Total', ascending=False).head(15)
        
        fig_zones = go.Figure()
        fig_zones.add_trace(go.Bar(
            name='Outflow (→ out)',
            y=zone_traffic_df['Zone'],
            x=zone_traffic_df['Outflow'],
            orientation='h',
            marker_color='#ef4444'
        ))
        fig_zones.add_trace(go.Bar(
            name='Inflow (← in)',
            y=zone_traffic_df['Zone'],
            x=zone_traffic_df['Inflow'],
            orientation='h',
            marker_color='#3b82f6'
        ))
        fig_zones.update_layout(
            title="Zone Traffic (Inflow vs Outflow)",
            barmode='group',
            xaxis_title="Transition Count",
            yaxis_title="",
            template="plotly_white",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_zones, use_container_width=True)
        
        # AI Interpretation for Traffic
        top_zone = zone_traffic_df.iloc[0]['Zone']
        top_total = zone_traffic_df.iloc[0]['Total']
        st.success(f"""
        🤖 **AI Insight**: **{top_zone}** is the highest-traffic zone with {top_total:,} total transitions.
        This zone is a **key traffic hub** - ideal for:
        - High-visibility advertising
        - Way-finding signage
        - Promotional displays
        """)
    
    st.markdown("---")
    
    # Section 4: Flow Map
    st.subheader("🗺️ Spatial Flow Map")
    
    with st.expander("ℹ️ How to read the Flow Map", expanded=False):
        st.markdown("""
        **The Flow Map visualizes zone-to-zone transitions on the actual floor plan.**
        
        - **Arrows** = Direction of movement (from → to)
        - **Arrow thickness** = Transition frequency (thicker = more traffic)
        - **Blue circles** = Zone centers
        
        **What to look for:**
        - Main corridors (thick arrows)
        - Bottlenecks (many arrows converging)
        - Dead zones (few or no arrows)
        """)
    
    map_img = load_map_image()
    
    if map_img is not None and sward_df is not None:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch, Circle
        import numpy as np
        import io
        
        # Get zone centers
        zone_centers = {}
        for zone in sward_df['description'].unique():
            zone_swards_list = sward_df[sward_df['description'] == zone]
            if len(zone_swards_list) > 0:
                center_x = zone_swards_list['x'].mean()
                center_y = zone_swards_list['y'].mean()
                zone_centers[zone] = (center_x, center_y)
        
        # Helper function to offset arrow endpoints
        def offset_point(x1, y1, x2, y2, offset=25):
            """Offset start/end points towards each other to avoid overlapping zone circles"""
            dx = x2 - x1
            dy = y2 - y1
            dist = np.sqrt(dx*dx + dy*dy)
            if dist < offset * 2:
                return x1, y1, x2, y2  # Too close, no offset
            # Normalize and offset
            nx, ny = dx / dist, dy / dist
            return x1 + nx * offset, y1 + ny * offset, x2 - nx * offset, y2 - ny * offset
        
        # Create figure
        fig_map, ax = plt.subplots(figsize=(16, 12))
        ax.imshow(map_img, aspect='auto')
        ax.axis('off')
        
        # Step 1: Draw ALL zone circles first (background layer)
        for zone, (x, y) in zone_centers.items():
            circle = Circle((x, y), radius=18, 
                           facecolor='#3b82f6', alpha=0.6,
                           edgecolor='white', linewidth=2, zorder=2)
            ax.add_patch(circle)
        
        # Step 2: Draw top flows as arrows (on top of circles)
        top_n_map = min(60, len(flow_agg))
        top_flows_map = flow_agg.head(top_n_map)
        max_count = top_flows_map['count'].max() if len(top_flows_map) > 0 else 1
        
        for _, row in top_flows_map.iterrows():
            from_zone = row['from_zone']
            to_zone = row['to_zone']
            count = row['count']
            
            if from_zone in zone_centers and to_zone in zone_centers:
                x1, y1 = zone_centers[from_zone]
                x2, y2 = zone_centers[to_zone]
                
                # Offset arrow endpoints to not overlap with zone circles
                ox1, oy1, ox2, oy2 = offset_point(x1, y1, x2, y2, offset=25)
                
                width = 2 + (count / max_count) * 8
                alpha = 0.5 + (count / max_count) * 0.4
                
                arrow = FancyArrowPatch(
                    (ox1, oy1), (ox2, oy2),
                    arrowstyle='->,head_width=0.6,head_length=0.5',
                    linewidth=width,
                    color='#ef4444',
                    alpha=alpha,
                    zorder=5,  # Above zone circles
                    mutation_scale=width * 0.75  # Scale arrow head with line width
                )
                ax.add_patch(arrow)
        
        # Step 3: Draw zone labels (topmost layer)
        for zone, (x, y) in zone_centers.items():
            ax.text(x, y - 28, zone, fontsize=14, fontweight='bold',
                   color='white', ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor='#1f2937', alpha=0.85, edgecolor='none'),
                   zorder=10)
        
        plt.title('Spatial Flow Patterns (All Zones)', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        buf = io.BytesIO()
        fig_map.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig_map)
        
        st.image(buf, use_container_width=True)
    else:
        st.warning("⚠️ Map image not available")


# =====================================================
# FLOW PREDICTION (Cache-based OutFlow/InFlow)
# =====================================================

def render_journey_prediction(date_str):
    """Render Flow Prediction - Cache-based OutFlow/InFlow Analysis"""
    st.title("🔮 Flow Prediction")
    
    # Load cached data (instant!)
    transitions_df = load_zone_transitions()
    zone_stats = load_zone_statistics()
    sward_df = load_sward_descriptions()
    
    if transitions_df is None:
        st.error("❌ Cache not found. Run `python src/precompute_journey_cache.py` first.")
        return
    
    # Philosophy explanation (collapsed by default)
    with st.expander("ℹ️ About Flow Prediction", expanded=False):
        st.markdown("""
        **Flow Prediction**은 Zone별 방문자 이동 패턴을 분석합니다:
        - **OutFlow**: 이 Zone에서 다음에 어디로 가나?
        - **InFlow**: 이 Zone으로 어디서 오나?
        
        맥락(요일/날씨/시간대)에 따라 패턴이 달라집니다.
        """)
    
    # ===== Compact Input Section =====
    st.markdown("### 🎯 Analysis Settings")
    
    # Row 1: Context + Zone Selection (all in one row)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.5])
    
    with col1:
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        selected_weekday = st.selectbox("📅 Weekday", weekday_names, index=0, key="pred_weekday")
        weekday_idx = weekday_names.index(selected_weekday)
    
    with col2:
        weather_options = ['Clear', 'Rainy', 'Cloudy']
        selected_weather = st.selectbox("☁️ Weather", weather_options, index=0, key="pred_weather")
    
    with col3:
        time_options = ['morning', 'afternoon', 'evening']
        time_labels = ['Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-22)']
        selected_time_label = st.selectbox("⏰ Time", time_labels, index=1, key="pred_time")
        time_bucket = time_options[time_labels.index(selected_time_label)]
    
    with col4:
        zones = sorted(transitions_df['from_zone'].unique().tolist())
        selected_zone = st.selectbox("🏪 Zone", zones, key="pred_zone")
    
    # Zone stats (compact)
    if zone_stats and selected_zone in zone_stats:
        zs = zone_stats[selected_zone]
        st.caption(f"📊 {selected_zone}: Visits {zs.get('total_visitors', 0):,} | Avg Dwell {zs.get('avg_dwell_time', 0):.0f}s | Inflow {zs.get('total_inflow', 0):,}")
    
    st.markdown("---")
    
    # ===== Results Section =====
    # Tabs for OutFlow and InFlow
    tab1, tab2 = st.tabs(["📤 OutFlow (Where to next?)", "📥 InFlow (Where from?)"])
    
    # Get zone centers for map
    zone_centers = {}
    if sward_df is not None:
        for zone in sward_df['description'].unique():
            zone_swards = sward_df[sward_df['description'] == zone]
            if len(zone_swards) > 0:
                zone_centers[zone] = (zone_swards['x'].mean(), zone_swards['y'].mean())
    
    with tab1:
        # Context display
        st.caption(f"Context: {selected_weekday}, {selected_weather}, {selected_time_label}")
        
        # Get outflow probabilities with fallback support
        outflow_probs, outflow_fallback_msg = get_zone_outflow_with_fallback(
            selected_zone, transitions_df, weekday_idx, selected_weather, time_bucket
        )
        
        # Display fallback message if applicable
        if outflow_fallback_msg:
            st.info(outflow_fallback_msg)
        
        if not outflow_probs:
            st.warning("⚠️ No outflow data for selected context. Try different settings.")
        else:
            # Sort by probability
            outflow_sorted = sorted(outflow_probs.items(), key=lambda x: -x[1])
            
            # Results first (Chart + Map)
            col_chart, col_map = st.columns([1, 1.5])
            
            with col_chart:
                # Bar chart
                outflow_df = pd.DataFrame(outflow_sorted, columns=['Zone', 'Probability'])
                outflow_df['Percentage'] = outflow_df['Probability'] * 100
                
                fig_out = go.Figure()
                fig_out.add_trace(go.Bar(
                    y=outflow_df['Zone'],
                    x=outflow_df['Percentage'],
                    orientation='h',
                    marker_color='#ef4444',
                    text=[f"{p:.1f}%" for p in outflow_df['Percentage']],
                    textposition='auto'
                ))
                fig_out.update_layout(
                    title=f"Outflow Probability from {selected_zone}",
                    xaxis_title="Probability (%)",
                    yaxis_title="",
                    template="plotly_white",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_out, use_container_width=True)
            
            with col_map:
                # Map visualization
                map_img = load_map_image()
                
                if map_img is not None and selected_zone in zone_centers:
                    import matplotlib.pyplot as plt
                    from matplotlib.patches import FancyArrowPatch, Circle
                    import numpy as np
                    import io
                    
                    # Helper function to offset arrow endpoints
                    def offset_point(x1, y1, x2, y2, offset=25):
                        dx = x2 - x1
                        dy = y2 - y1
                        dist = np.sqrt(dx*dx + dy*dy)
                        if dist < offset * 2:
                            return x1, y1, x2, y2
                        nx, ny = dx / dist, dy / dist
                        return x1 + nx * offset, y1 + ny * offset, x2 - nx * offset, y2 - ny * offset
                    
                    fig_map, ax = plt.subplots(figsize=(12, 9))
                    ax.imshow(map_img, aspect='auto')
                    ax.axis('off')
                    
                    # Step 1: Draw ALL zone circles (background)
                    for zone, (x, y) in zone_centers.items():
                        if zone == selected_zone:
                            continue  # Skip source zone, draw it later
                        circle = Circle((x, y), radius=15, 
                                       facecolor='#6b7280', alpha=0.4,
                                       edgecolor='white', linewidth=1, zorder=2)
                        ax.add_patch(circle)
                        ax.text(x, y - 26, zone, fontsize=12, fontweight='bold',
                               color='white', ha='center', va='bottom',
                               bbox=dict(boxstyle='round,pad=0.25', facecolor='#374151', alpha=0.7, edgecolor='none'),
                               zorder=3)
                    
                    # Step 2: Draw arrows to destinations
                    src_x, src_y = zone_centers[selected_zone]
                    max_prob = max(outflow_probs.values()) if outflow_probs else 1
                    
                    for dest_zone, prob in outflow_sorted[:10]:  # Top 10
                        if dest_zone in zone_centers:
                            dst_x, dst_y = zone_centers[dest_zone]
                            ox1, oy1, ox2, oy2 = offset_point(src_x, src_y, dst_x, dst_y, offset=28)
                            
                            width = 2 + (prob / max_prob) * 6
                            alpha = 0.4 + (prob / max_prob) * 0.5
                            
                            arrow = FancyArrowPatch(
                                (ox1, oy1), (ox2, oy2),
                                arrowstyle='->,head_width=0.6,head_length=0.5',
                                linewidth=width,
                                color='#ef4444',
                                alpha=alpha,
                                zorder=5,
                                mutation_scale=width * 0.75
                            )
                            ax.add_patch(arrow)
                            
                            # Highlight destination zone
                            circle = Circle((dst_x, dst_y), radius=15, 
                                           facecolor='#3b82f6', alpha=0.8,
                                           edgecolor='white', linewidth=2, zorder=6)
                            ax.add_patch(circle)
                            ax.text(dst_x, dst_y + 22, f"{prob*100:.1f}%", fontsize=9, fontweight='bold',
                                   color='#ef4444', ha='center', va='top', zorder=8)
                    
                    # Step 3: Draw source zone (topmost)
                    circle = Circle((src_x, src_y), radius=20, 
                                   facecolor='#ef4444', alpha=0.9,
                                   edgecolor='white', linewidth=3, zorder=10)
                    ax.add_patch(circle)
                    ax.text(src_x, src_y - 35, selected_zone, fontsize=20, fontweight='bold',
                           color='white', ha='center', va='bottom',
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ef4444', alpha=0.9, edgecolor='none'),
                           zorder=11)
                    
                    plt.title(f'OutFlow from {selected_zone} (All Zones Shown)', fontsize=14, fontweight='bold', pad=15)
                    plt.tight_layout()
                    
                    buf = io.BytesIO()
                    fig_map.savefig(buf, format='png', dpi=120, bbox_inches='tight')
                    buf.seek(0)
                    plt.close(fig_map)
                    
                    st.image(buf, use_container_width=True)
                else:
                    st.warning("Map visualization not available")
            
            # AI Insight AFTER results
            if len(outflow_sorted) >= 2:
                top_dest = outflow_sorted[0][0]
                top_prob = outflow_sorted[0][1] * 100
                second_dest = outflow_sorted[1][0]
                second_prob = outflow_sorted[1][1] * 100
                
                # Special case handling for Entrance/Self-checkout
                selected_lower = selected_zone.lower()
                top_dest_lower = top_dest.lower()
                
                # Self-checkout → Entrance: 퇴장 동선
                if 'checkout' in selected_lower and 'entrance' in top_dest_lower:
                    st.success(f"""
                    🤖 **AI Insight**: **{selected_zone}**에서 **{top_dest}** 방향으로 **{top_prob:.1f}%**가 이동합니다.
                    
                    ⚠️ **해석 주의**: 이는 **퇴장 동선**으로 해석됩니다. 계산 후 에스컬레이터/카트 보관소로 이동하는 고객 흐름입니다.
                    Entrance 구역의 S-Ward 커버리지가 넓어 인접 통로 이동도 포함될 수 있습니다.
                    
                    💡 출구 동선에 **재방문 유도 쿠폰** 또는 **다음 방문 프로모션** 배치를 고려하세요.
                    """)
                # Entrance → Self-checkout: 비정상적 패턴 (빠른 퇴장)
                elif 'entrance' in selected_lower and 'checkout' in top_dest_lower:
                    st.warning(f"""
                    🤖 **AI Insight**: **{selected_zone}**에서 **{top_dest}** 방향으로 **{top_prob:.1f}%**가 이동합니다.
                    
                    ⚠️ **해석 주의**: 입구에서 바로 계산대로 이동하는 패턴입니다. 
                    이는 **목적 구매 고객**(특정 상품만 구매) 또는 **S-Ward 커버리지 오버랩**으로 인한 노이즈일 수 있습니다.
                    
                    💡 입구 근처에 **신상품/프로모션 존** 배치로 체류시간 증가를 유도하세요.
                    """)
                # Entrance 관련 일반 케이스
                elif 'entrance' in top_dest_lower:
                    st.info(f"""
                    🤖 **AI Insight**: **{selected_zone}**에서 **{top_prob:.1f}%**가 **{top_dest}** 방향으로 이동합니다.
                    
                    ℹ️ **참고**: Entrance 구역은 S-Ward 커버리지가 넓어, 실제로는 **입구 방향 통로 이동**을 의미할 수 있습니다.
                    2위 목적지 **{second_dest}** ({second_prob:.1f}%)도 함께 고려하세요.
                    """)
                # 일반 케이스
                else:
                    st.success(f"""
                    🤖 **AI Insight**: **{selected_zone}**에서 출발하는 방문자의 **{top_prob:.1f}%**가 
                    **{top_dest}**로 이동합니다. 2위는 **{second_dest}** ({second_prob:.1f}%).
                    
                    💡 {top_dest}와 연계 마케팅 강화 또는 {second_dest}로의 유도 증가를 고려하세요.
                    """)
    
    with tab2:
        # Context display
        st.caption(f"Context: {selected_weekday}, {selected_weather}, {selected_time_label}")
        
        # Get inflow probabilities with fallback support
        inflow_probs, inflow_fallback_msg = get_zone_inflow_with_fallback(
            selected_zone, transitions_df, weekday_idx, selected_weather, time_bucket
        )
        
        # Display fallback message if applicable
        if inflow_fallback_msg:
            st.info(inflow_fallback_msg)
        
        if not inflow_probs:
            st.warning("⚠️ No inflow data for selected context. Try different settings.")
        else:
            # Sort by probability
            inflow_sorted = sorted(inflow_probs.items(), key=lambda x: -x[1])
            
            # Results first (Chart + Map)
            col_chart, col_map = st.columns([1, 1.5])
            
            with col_chart:
                # Bar chart
                inflow_df = pd.DataFrame(inflow_sorted, columns=['Zone', 'Probability'])
                inflow_df['Percentage'] = inflow_df['Probability'] * 100
                
                fig_in = go.Figure()
                fig_in.add_trace(go.Bar(
                    y=inflow_df['Zone'],
                    x=inflow_df['Percentage'],
                    orientation='h',
                    marker_color='#3b82f6',
                    text=[f"{p:.1f}%" for p in inflow_df['Percentage']],
                    textposition='auto'
                ))
                fig_in.update_layout(
                    title=f"Inflow Probability to {selected_zone}",
                    xaxis_title="Probability (%)",
                    yaxis_title="",
                    template="plotly_white",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_in, use_container_width=True)
            
            with col_map:
                # Map visualization
                map_img = load_map_image()
                
                if map_img is not None and selected_zone in zone_centers:
                    import matplotlib.pyplot as plt
                    from matplotlib.patches import FancyArrowPatch, Circle
                    import numpy as np
                    import io
                    
                    # Helper function to offset arrow endpoints
                    def offset_point(x1, y1, x2, y2, offset=25):
                        dx = x2 - x1
                        dy = y2 - y1
                        dist = np.sqrt(dx*dx + dy*dy)
                        if dist < offset * 2:
                            return x1, y1, x2, y2
                        nx, ny = dx / dist, dy / dist
                        return x1 + nx * offset, y1 + ny * offset, x2 - nx * offset, y2 - ny * offset
                    
                    fig_map, ax = plt.subplots(figsize=(12, 9))
                    ax.imshow(map_img, aspect='auto')
                    ax.axis('off')
                    
                    # Step 1: Draw ALL zone circles (background)
                    for zone, (x, y) in zone_centers.items():
                        if zone == selected_zone:
                            continue  # Skip target zone, draw it later
                        circle = Circle((x, y), radius=15, 
                                       facecolor='#6b7280', alpha=0.4,
                                       edgecolor='white', linewidth=1, zorder=2)
                        ax.add_patch(circle)
                        ax.text(x, y - 26, zone, fontsize=12, fontweight='bold',
                               color='white', ha='center', va='bottom',
                               bbox=dict(boxstyle='round,pad=0.25', facecolor='#374151', alpha=0.7, edgecolor='none'),
                               zorder=3)
                    
                    # Step 2: Draw arrows from sources
                    dst_x, dst_y = zone_centers[selected_zone]
                    max_prob = max(inflow_probs.values()) if inflow_probs else 1
                    
                    for src_zone, prob in inflow_sorted[:10]:  # Top 10
                        if src_zone in zone_centers:
                            src_x, src_y = zone_centers[src_zone]
                            ox1, oy1, ox2, oy2 = offset_point(src_x, src_y, dst_x, dst_y, offset=28)
                            
                            width = 2 + (prob / max_prob) * 6
                            alpha = 0.4 + (prob / max_prob) * 0.5
                            
                            arrow = FancyArrowPatch(
                                (ox1, oy1), (ox2, oy2),
                                arrowstyle='->,head_width=0.6,head_length=0.5',
                                linewidth=width,
                                color='#3b82f6',
                                alpha=alpha,
                                zorder=5,
                                mutation_scale=width * 0.75
                            )
                            ax.add_patch(arrow)
                            
                            # Highlight source zone
                            circle = Circle((src_x, src_y), radius=15, 
                                           facecolor='#10b981', alpha=0.8,
                                           edgecolor='white', linewidth=2, zorder=6)
                            ax.add_patch(circle)
                            ax.text(src_x, src_y + 22, f"{prob*100:.1f}%", fontsize=9, fontweight='bold',
                                   color='#3b82f6', ha='center', va='top', zorder=8)
                    
                    # Step 3: Draw target zone (topmost)
                    circle = Circle((dst_x, dst_y), radius=20, 
                                   facecolor='#3b82f6', alpha=0.9,
                                   edgecolor='white', linewidth=3, zorder=10)
                    ax.add_patch(circle)
                    ax.text(dst_x, dst_y - 35, selected_zone, fontsize=20, fontweight='bold',
                           color='white', ha='center', va='bottom',
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='#3b82f6', alpha=0.9, edgecolor='none'),
                           zorder=11)
                    
                    plt.title(f'InFlow to {selected_zone} (All Zones Shown)', fontsize=14, fontweight='bold', pad=15)
                    plt.tight_layout()
                    
                    buf = io.BytesIO()
                    fig_map.savefig(buf, format='png', dpi=120, bbox_inches='tight')
                    buf.seek(0)
                    plt.close(fig_map)
                    
                    st.image(buf, use_container_width=True)
                else:
                    st.warning("Map visualization not available")
            
            # AI Insight AFTER results
            if len(inflow_sorted) >= 2:
                top_src = inflow_sorted[0][0]
                top_prob = inflow_sorted[0][1] * 100
                second_src = inflow_sorted[1][0]
                second_prob = inflow_sorted[1][1] * 100
                
                # Special case handling for Entrance/Self-checkout
                selected_lower = selected_zone.lower()
                top_src_lower = top_src.lower()
                
                # Entrance ← Self-checkout: 퇴장 동선 역방향
                if 'entrance' in selected_lower and 'checkout' in top_src_lower:
                    st.success(f"""
                    🤖 **AI Insight**: **{selected_zone}** 구역으로 **{top_prob:.1f}%**가 **{top_src}**에서 유입됩니다.
                    
                    ⚠️ **해석 주의**: 이는 **퇴장 고객 흐름**입니다. 계산 후 출구/에스컬레이터로 이동하는 동선입니다.
                    Entrance S-Ward의 넓은 커버리지로 인해 출구 방향 통로 이동이 포함됩니다.
                    
                    💡 퇴장 동선에 **재방문 쿠폰**, **멤버십 가입 안내** 등을 배치하세요.
                    """)
                # Self-checkout ← Entrance: 입장 후 바로 계산대
                elif 'checkout' in selected_lower and 'entrance' in top_src_lower:
                    st.warning(f"""
                    🤖 **AI Insight**: **{selected_zone}**으로 **{top_prob:.1f}%**가 **{top_src}**에서 직접 유입됩니다.
                    
                    ⚠️ **해석 주의**: 입구에서 바로 계산대로 오는 패턴입니다.
                    **목적 구매 고객** 또는 **Entrance S-Ward 커버리지 오버랩**으로 인한 노이즈일 수 있습니다.
                    2위 유입원 **{second_src}** ({second_prob:.1f}%)가 더 의미 있는 분석 대상일 수 있습니다.
                    
                    💡 계산대 근처에 **충동구매 상품** 배치로 객단가 증가를 유도하세요.
                    """)
                # Entrance에서 유입되는 일반 케이스
                elif 'entrance' in top_src_lower:
                    st.info(f"""
                    🤖 **AI Insight**: **{selected_zone}**으로 **{top_prob:.1f}%**가 **{top_src}**에서 유입됩니다.
                    
                    ℹ️ **참고**: Entrance는 S-Ward 커버리지가 넓어 **입구 방향에서 온 모든 고객**을 포함합니다.
                    실제 직전 경유지는 2위 **{second_src}** ({second_prob:.1f}%)가 더 정확할 수 있습니다.
                    
                    💡 {second_src}에 {selected_zone} 관련 안내를 배치하면 유입 증대가 가능합니다.
                    """)
                # 일반 케이스
                else:
                    st.success(f"""
                    🤖 **AI Insight**: **{selected_zone}**을 방문하는 사람들의 **{top_prob:.1f}%**가 
                    **{top_src}**에서 옵니다. 2위는 **{second_src}** ({second_prob:.1f}%).
                    
                    💡 {top_src}에 {selected_zone} 관련 프로모션/안내를 배치하면 유입 증대가 가능합니다.
                    """)

# =====================================================
# MAIN APP
# =====================================================

def main():
    """Main application entry point"""
    
    # Render sidebar and get selections
    selected_date, selected_menu = render_sidebar()
    
    if not selected_date or not selected_menu:
        st.info("Please select a date from the sidebar to begin")
        return
    
    # Route to appropriate page based on menu selection
    if "Traffic Analysis" in selected_menu:
        render_traffic_analysis(selected_date)
    elif "Localization" in selected_menu:
        render_localization(selected_date)
    elif "Heatmap Analysis" in selected_menu:
        render_heatmap_analysis(selected_date)
    elif "Spatial Flow" in selected_menu:
        render_journey_analysis(selected_date)
    elif "Flow Prediction" in selected_menu:
        render_journey_prediction(selected_date)

if __name__ == "__main__":
    main()

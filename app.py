import streamlit as st
import json
import os
import glob
import time
import pipeline

st.set_page_config(page_title="Nova Autonomous Agent", page_icon="⚡", layout="wide")

# ============================================
# STYLE & AESTHETICS (PREMIUM DARK MODE)
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* Global settings */
    .stApp {
        background-color: #0b0f14;
        background-image: radial-gradient(rgba(232, 169, 76, 0.05) 1px, transparent 1px);
        background-size: 24px 24px;
        color: #e6edf3;
        font-family: 'Outfit', sans-serif;
    }
    
    header, [data-testid="stHeader"], .stAppHeader { 
        visibility: hidden !important; 
        display: none !important; 
    }
    
    /* Remove default Streamlit huge padding that causes scrolling */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Opening effect for the welcome page */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Center the welcome page without causing overflow scroll */
    .welcome-container {
        animation: fadeInUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1);
        margin-top: 8vh;
        margin-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
        font-weight: 600;
    }

    /* Primary text styling */
    .amber-text {
        color: #E8A94C;
        font-weight: 700;
    }
    
    .subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(232, 169, 76, 0.15);
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
        margin: 1rem auto;
    }

    .evaluation-card {
        background: #12161c;
        border: 1px solid #30363d;
        border-top: 3px solid #E8A94C;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    .badge-amber { background: rgba(232, 169, 76, 0.1); color: #E8A94C; border: 1px solid rgba(232, 169, 76, 0.3); }

    /* Inputs */
    div[data-baseweb="slider"] {
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, #E8A94C, #d49132);
        color: #0b0f14;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d49132, #c07a1b);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(232, 169, 76, 0.3);
        color: #0b0f14;
    }
    .stButton > button:active { color: #0b0f14; }

    /* Tags for results */
    .card-tag {
        font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem;
        letter-spacing: 0.14em; color: #E8A94C; text-transform: uppercase;
        border-left: 2px solid #E8A94C; padding-left: 0.6rem; margin-bottom: 0.9rem;
    }
    .field-label {
        font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem;
        letter-spacing: 0.1em; color: #8b949e; text-transform: uppercase;
        margin-top: 0.7rem;
    }
    .mood-badge {
        display: inline-block; border: 1px solid #3a3527; color: #E8A94C;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem; padding: 0.14rem 0.55rem; border-radius: 3px;
        margin: 0.15rem 0.15rem 0.15rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "num_videos" not in st.session_state:
    st.session_state.num_videos = 3


# ============================================
# PHASE 1: WELCOME STAGE
# ============================================
def welcome_stage():
    # Empty space to push content down manually instead of CSS flexbox wrapping
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Thumbnail image
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image("nova_thumbnail.png", width="stretch")
            
        st.markdown('<h1 style="font-size:2.8rem; margin-top:1rem; text-align:center;">Welcome to <span class="amber-text">Nova</span></h1>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle" style="text-align:center;">Your Autonomous AI Video Broadcast Agent.</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Enter Dashboard 🚀"):
            st.session_state.phase = 2
            st.rerun()


# ============================================
# PHASE 2: CONFIGURATION STAGE (COMMAND CENTER)
# ============================================
def config_stage():
    # Inject specific styles for the dashboard
    st.markdown("""
    <style>
        .stat-card {
            background: rgba(22, 27, 34, 0.4);
            border: 1px solid rgba(232, 169, 76, 0.15);
            border-radius: 12px;
            padding: 1.8rem;
            text-align: center;
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: rgba(232, 169, 76, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(232, 169, 76, 0.1);
        }
        .stat-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.8rem;
        }
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #2ea043;
            box-shadow: 0 0 12px #2ea043;
            margin-right: 8px;
        }
        .status-text {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            color: #2ea043;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .config-header {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.4rem;
            color: #E8A94C;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid rgba(232, 169, 76, 0.2);
            padding-bottom: 0.5rem;
        }
        
        /* Make the main button huge */
        .big-btn button {
            padding: 1.2rem !important;
            font-size: 1.1rem !important;
            letter-spacing: 0.1em !important;
            box-shadow: 0 0 20px rgba(232, 169, 76, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="badge badge-amber">COMMAND CENTER</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 2.5rem; margin-top: 0; margin-bottom: 0.5rem;">System Overview</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8b949e; font-size:1.1rem;">All core modules are online. Configure your next autonomous broadcast run.</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # YouTube Data Integration Status
    st.markdown('''
    <div style="background: rgba(22, 27, 34, 0.4); border: 1px solid rgba(232, 169, 76, 0.3); border-radius: 12px; padding: 1.8rem; text-align: center; margin-bottom: 1.5rem;">
        <h3 style="color:#E8A94C; font-family:'Space Grotesk', sans-serif; margin-bottom: 0.5rem;">YouTube Live Sync</h3>
        <p style="color:#e6edf3; font-size:1.1rem; margin-bottom: 0;">
            <span class="status-dot"></span> Reliably fetching latest Shorts data directly from YouTube.
        </p>
    </div>
    ''', unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Configuration Section
    st.markdown('<div class="config-header">Broadcast Parameters</div>', unsafe_allow_html=True)
    
    cc1, cc2 = st.columns([2, 1])
    with cc1:
        st.markdown('<p style="color:#e6edf3; font-weight:500; font-size:1.1rem; margin-bottom:0.2rem;">Target Intake Volume</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#8b949e; font-size:0.9rem;">Select the number of trending shorts to automatically fetch, analyze, and convert.</p>', unsafe_allow_html=True)
        num = st.slider("Target Intake Volume", min_value=1, max_value=10, value=st.session_state.num_videos, label_visibility="collapsed")
        st.session_state.num_videos = num
    
    with cc2:
        st.markdown('<p style="color:#e6edf3; font-weight:500; font-size:1.1rem; margin-bottom:0.2rem;">Engine Overrides</p>', unsafe_allow_html=True)
        force = st.checkbox("Force Regenerate (Ignore Cache)", value=st.session_state.get('force_regenerate', False))
        st.session_state.force_regenerate = force
        st.caption("Completely re-renders output, ignoring cached archives.")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Huge action button
    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("INITIATE AUTONOMOUS BROADCAST 🚀"):
            st.session_state.phase = 3
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# PHASE 3: GENERATION & RESULTS STAGE
# ============================================
def results_stage():
    st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="badge badge-amber">Phase 03</div>', unsafe_allow_html=True)
    st.markdown('<h2>Live Broadcast & Results</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        if "completed" not in st.session_state:
            # RUN PIPELINE
            st.markdown('<h3 style="color:#ff5c5c; margin-top:0; text-align:center;">◉ ON AIR — SCANNING SIGNALS</h3>', unsafe_allow_html=True)
            
            with st.status("Scanning YouTube...", expanded=True) as fetch_status:
                shorts = pipeline.get_trending_shorts(max_results=st.session_state.num_videos)
                if not shorts:
                    fetch_status.update(label="No signal found — check your YouTube API key/quota.", state="error")
                    st.stop()
                for v in shorts:
                    st.write(f"• {v['title']}")
                fetch_status.update(label=f"Picked up {len(shorts)} trending signals", state="complete")

            progress_bar = st.progress(0, text="Starting Generation...")
            results = []

            for i, video in enumerate(shorts, start=1):
                json_path = f"output_{i}.json"

                if not st.session_state.force_regenerate and os.path.exists(json_path):
                    progress_bar.progress(i / len(shorts), text=f"Signal {i} already archived, skipping")
                    results.append({
                        "json": json_path,
                        "image": f"generated_image_{i}.png",
                        "video": f"output_video_{i}.mp4",
                    })
                    continue

                with st.status(f"Signal {i}: {video['title']}", expanded=True) as status:
                    def update(msg, s=status, idx=i):
                        try:
                            s.update(label=f"Signal {idx}: {msg}")
                            st.write(msg)
                        except RuntimeError:
                            # Streamlit event loop is closed (user refreshed or stopped)
                            pass

                    outcome = pipeline.process_video(video, i, progress_callback=update)
                    if outcome:
                        status.update(label=f"Signal {i}: broadcast", state="complete")
                        results.append(outcome)
                    else:
                        status.update(label=f"Signal {i}: lost signal", state="error")

                progress_bar.progress(i / len(shorts), text=f"{i}/{len(shorts)} processed")

            progress_bar.empty()
            st.success(f"Off air — {len(results)}/{len(shorts)} signals broadcast.")
            st.session_state.completed = True
            time.sleep(1)
            st.rerun()
            
        else:
            # SHOW RESULTS (Archive format in glassmorphism)
            json_files = sorted(glob.glob("output_*.json"))
            
            if not json_files:
                st.info("No generated files found.")
            else:
                for json_path in json_files:
                    index = json_path.replace("output_", "").replace(".json", "")

                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    image_path = f"generated_image_{index}.png"
                    video_path = f"output_video_{index}.mp4"

                    st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-tag">Broadcast {index}</div>', unsafe_allow_html=True)

                    inner_c1, inner_c2, inner_c3 = st.columns([1, 1, 1.2])

                    with inner_c1:
                        if os.path.exists(image_path):
                            st.image(image_path, caption="Frame")
                        else:
                            st.warning("Image not found")

                    with inner_c2:
                        if os.path.exists(video_path):
                            st.video(video_path)
                        else:
                            st.warning("Video not found")

                    with inner_c3:
                        st.markdown('<div class="field-label">Image prompt</div>', unsafe_allow_html=True)
                        st.caption(data.get("image_prompt", "N/A"))
                        st.markdown('<div class="field-label">Video prompt</div>', unsafe_allow_html=True)
                        st.caption(data.get("video_prompt", "N/A"))

                        moods = [s.get("mood", "") for s in data.get("scenes", []) if s.get("mood")]
                        if moods:
                            st.markdown('<div class="field-label">Mood</div>', unsafe_allow_html=True)
                            badges = "".join(f'<span class="mood-badge">{m}</span>' for m in moods)
                            st.markdown(badges, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Start New Session"):
                st.session_state.phase = 1
                if "completed" in st.session_state:
                    del st.session_state.completed
                st.rerun()


# ============================================
# MAIN ROUTING
# ============================================
if st.session_state.phase == 1:
    welcome_stage()
elif st.session_state.phase == 2:
    config_stage()
elif st.session_state.phase == 3:
    results_stage()
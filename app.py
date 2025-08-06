# filename: elegant_arabic_transcriber.py

import streamlit as st
import nemo.collections.asr as nemo_asr
import soundfile as sf
import tempfile
import os
from pydub import AudioSegment
import time

# Custom CSS for gloomy elegant styling
st.markdown("""
    <style>
        :root {
            --primary: #3a506b;
            --secondary: #5bc0be;
            --accent: #e55934;
            --background: #1c2541;
            --card: #0b132b;
            --text: #e0e0e0;
            --text-secondary: #b8b8b8;
        }
        
        .stApp {
            background-color: var(--background);
            color: var(--text);
        }
        
        .main .block-container {
            max-width: 1200px;
            padding: 2rem 3rem;
        }
        
        .card {
            background-color: var(--card);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 3px solid var(--secondary);
        }
        
        .header {
            background: linear-gradient(135deg, #0b132b, #1c2541);
            color: white;
            padding: 2rem 3rem;
            margin: -2rem -3rem 2rem -3rem;
            border-bottom: 1px solid rgba(91, 192, 190, 0.2);
        }
        
        .stButton>button {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.7rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid rgba(91, 192, 190, 0.3);
        }
        
        .stButton>button:hover {
            background: #2c3e5a;
            color: white;
        }
        
        .stDownloadButton>button {
            background: var(--secondary);
            color: #0b132b;
        }
        
        .stDownloadButton>button:hover {
            background: #4aa8a6;
            color: #0b132b;
        }
        
        .transcript-container {
            background-color: rgba(11, 19, 43, 0.7);
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1rem;
            border: 1px solid rgba(91, 192, 190, 0.1);
        }
        
        .transcript-box {
            background-color: transparent;
            font-size: 1.1rem;
            line-height: 1.8;
            min-height: 150px;
            direction: rtl;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text);
            white-space: pre-wrap;
        }
        
        .stats {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .stat-box {
            background-color: rgba(58, 80, 107, 0.5);
            padding: 0.8rem 1rem;
            border-radius: 6px;
            flex: 1;
            min-width: 100px;
            text-align: center;
            border: 1px solid rgba(91, 192, 190, 0.1);
        }
        
        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--secondary);
        }
        
        .progress-container {
            height: 6px;
            background-color: rgba(58, 80, 107, 0.5);
            border-radius: 3px;
            margin: 1.5rem 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--secondary), #4aa8a6);
            border-radius: 3px;
            transition: width 0.4s ease;
        }
        
        h1, h2, h3 {
            color: var(--text) !important;
        }
        
        .file-uploader {
            border: 2px dashed var(--secondary);
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            background-color: rgba(91, 192, 190, 0.05);
            margin-bottom: 1.5rem;
        }
        
        .feature-icon {
            color: var(--secondary);
            margin-right: 0.5rem;
        }
        
        .stSpinner > div {
            border-color: var(--secondary) transparent transparent transparent !important;
        }
    </style>
""", unsafe_allow_html=True)

SUPPORTED_TYPES = ['wav', 'mp3', 'ogg', 'flac', 'm4a']

# Load NeMo model once
@st.cache_resource
def load_model():
    model = nemo_asr.models.EncDecHybridRNNTCTCBPEModel.from_pretrained(
        model_name="nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0"
    )
    return model

model = load_model()

# Helper: Convert any audio to 16kHz mono WAV
def convert_audio(uploaded_file, target_sample_rate=16000):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_out:
        audio = AudioSegment.from_file(uploaded_file)
        audio = audio.set_frame_rate(target_sample_rate).set_channels(1)
        audio.export(tmp_out.name, format="wav")
        return tmp_out.name

# App UI
st.markdown("""
    <div class="header">
        <h1 style="margin-bottom: 0.5rem;">Arabic Transcriber</h1>
        <p style="color: var(--text-secondary); margin-top: 0;">Convert speech to text with precision</p>
    </div>
""", unsafe_allow_html=True)

# Main content - single wide column layout
st.markdown("""
    <div class="card">
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <span class="feature-icon">🔊</span>
            <span>Supports WAV, MP3, OGG, FLAC, M4A</span>
        </div>
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <span class="feature-icon">⚡</span>
            <span>Fast processing with advanced AI</span>
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Drag and drop audio file here", type=SUPPORTED_TYPES)

if uploaded_file is not None:
    # Convert to 16kHz mono wav
    with st.spinner("Preparing audio for transcription..."):
        processed_wav = convert_audio(uploaded_file)
    
    # Show audio info
    data, sample_rate = sf.read(processed_wav)
    channels = 1 if len(data.shape) == 1 else data.shape[1]
    duration = len(data) / sample_rate
    
    # Show audio player and info
    st.audio(processed_wav, format="audio/wav")
    
    st.markdown("### Audio Details")
    st.markdown("""
        <div class="stats">
            <div class="stat-box">
                <div>Duration</div>
                <div class="stat-value">{:.1f}s</div>
            </div>
            <div class="stat-box">
                <div>Sample Rate</div>
                <div class="stat-value">{} Hz</div>
            </div>
            <div class="stat-box">
                <div>Channels</div>
                <div class="stat-value">{}</div>
            </div>
        </div>
    """.format(duration, sample_rate, channels), unsafe_allow_html=True)
    
    # Transcription
    if st.button("Transcribe Audio", type="primary"):
        # Create a progress container
        progress_container = st.empty()
        progress_container.markdown("""
            <div class="progress-container">
                <div class="progress-bar" style="width: 30%;"></div>
            </div>
            <div style="text-align: center; margin-top: 5px; color: var(--secondary);">Processing audio...</div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.8)
        progress_container.markdown("""
            <div class="progress-container">
                <div class="progress-bar" style="width: 70%;"></div>
            </div>
            <div style="text-align: center; margin-top: 5px; color: var(--secondary);">Transcribing content...</div>
        """, unsafe_allow_html=True)
        
        # Actual transcription
        with st.spinner(""):
            result = model.transcribe([processed_wav])
            transcript = result[0].text
        
        # Update progress to complete
        progress_container.markdown("""
            <div class="progress-container">
                <div class="progress-bar" style="width: 100%;"></div>
            </div>
            <div style="text-align: center; margin-top: 5px; color: var(--secondary);">Transcription complete</div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        progress_container.empty()
        
        st.markdown("### Transcription Results")
        st.markdown(f"""
            <div class="transcript-container">
                <div class="transcript-box">{transcript}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Download button
        st.download_button("Download Transcript", transcript, 
                          file_name="arabic_transcript.txt")
        
        # Cleanup
        os.remove(processed_wav)

# Minimal footer
st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); padding: 2rem 0; font-size: 0.8rem;">
        <p>Powered by NeMo ASR • Secure local processing</p>
    </div>
""", unsafe_allow_html=True)
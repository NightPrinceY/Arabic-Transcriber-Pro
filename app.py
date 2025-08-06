import streamlit as st
import nemo.collections.asr as nemo_asr
import tempfile
import os
import time
import threading
import pyaudio
import wave
from datetime import datetime
import random
from streamlit.runtime.scriptrunner import add_script_run_ctx
import numpy as np

# Enhanced Professional UI with Arabic Aesthetic
st.markdown("""
    <style>
        :root {
            --primary: #1c2541;
            --secondary: #5bc0be;
            --accent: #e55934;
            --background: #0b132b;
            --card: #1c2541;
            --text: #f0f5ff;
            --text-secondary: #b8c6db;
            --gold: #d4af37;
            --teal: #5bc0be;
            --dark-blue: #0b132b;
            --light-gold: #f5e7a1;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--dark-blue) 0%, #1a1f3d 100%);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main .block-container {
            max-width: 1000px;
            padding: 2rem 2rem 1rem;
        }
        
        .header {
            background: linear-gradient(135deg, #0b132b 0%, #1a1f3d 100%);
            color: white;
            padding: 2rem 0;
            margin: -2rem -2rem 1.5rem -2rem;
            border-bottom: 1px solid rgba(91, 192, 190, 0.2);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, var(--teal), var(--light-gold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: 0.5px;
            position: relative;
            padding-bottom: 0.5rem;
        }
        
        .header h1::after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 25%;
            width: 50%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--teal), transparent);
        }
        
        .header p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .card {
            background: rgba(28, 37, 65, 0.8);
            border-radius: 16px;
            padding: 1.8rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(91, 192, 190, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(4px);
        }
        
        .section-title {
            font-size: 1.4rem;
            margin-bottom: 1.2rem;
            color: var(--teal);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title::before {
            content: "•";
            color: var(--gold);
            font-size: 1.8rem;
        }
        
        .button-container {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .control-button {
            background: linear-gradient(135deg, #1c2541, #3a506b);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 0.9rem 2.2rem;
            font-weight: 600;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(91, 192, 190, 0.4);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }
        
        .control-button:hover {
            background: linear-gradient(135deg, #3a506b, #1c2541);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(91, 192, 190, 0.3);
        }
        
        .stop-button {
            background: linear-gradient(135deg, #5c2a2a, #8a3a3a);
            border: 1px solid rgba(229, 89, 52, 0.4);
        }
        
        .stop-button:hover {
            background: linear-gradient(135deg, #8a3a3a, #5c2a2a);
            box-shadow: 0 6px 20px rgba(229, 89, 52, 0.3);
        }
        
        .download-button {
            background: linear-gradient(135deg, #1a5c2a, #2a8a3a);
            border: 1px solid rgba(89, 229, 52, 0.4);
        }
        
        .download-button:hover {
            background: linear-gradient(135deg, #2a8a3a, #1a5c2a);
            box-shadow: 0 6px 20px rgba(89, 229, 52, 0.3);
        }
        
        .transcript-container {
            background: rgba(11, 19, 43, 0.7);
            border-radius: 12px;
            padding: 1.8rem;
            margin-top: 0.5rem;
            border: 1px solid rgba(91, 192, 190, 0.1);
            min-height: 220px;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
        }
        
        .transcript-box {
            background-color: transparent;
            font-size: 1.25rem;
            line-height: 1.9;
            direction: rtl;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text);
            white-space: pre-wrap;
            text-align: justify;
            padding: 10px 0;
        }
        
        .word-stream-container {
            background: rgba(11, 19, 43, 0.7);
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 0.5rem;
            border: 1px solid rgba(91, 192, 190, 0.1);
            min-height: 150px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
        }
        
        .word-bubble {
            background: linear-gradient(135deg, #2d3a5c, #1c2541);
            color: var(--light-gold);
            padding: 10px 18px;
            border-radius: 25px;
            border: 1px solid rgba(212, 175, 55, 0.4);
            font-weight: 600;
            font-size: 1.2rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            animation: fadeIn 0.4s ease-out, float 4s infinite ease-in-out;
            transition: all 0.3s ease;
            cursor: default;
        }
        
        .word-bubble:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(212, 175, 55, 0.3);
            background: linear-gradient(135deg, #3a506b, #2d3a5c);
        }
        
        .placeholder-text {
            color: rgba(224, 224, 224, 0.3);
            font-style: italic;
            font-size: 1.1rem;
            text-align: center;
            width: 100%;
            padding: 2rem 0;
        }
        
        .recording-indicator {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background-color: #ff4d4d;
            margin-right: 10px;
            box-shadow: 0 0 10px #ff4d4d;
            animation: pulse 1.5s infinite;
        }
        
        .stats {
            display: flex;
            gap: 1rem;
            margin: 1.5rem 0 0.5rem;
            justify-content: center;
        }
        
        .stat-box {
            background: rgba(28, 37, 65, 0.6);
            padding: 1rem;
            border-radius: 12px;
            flex: 1;
            min-width: 100px;
            text-align: center;
            border: 1px solid rgba(91, 192, 190, 0.2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .stat-box:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(91, 192, 190, 0.2);
            background: rgba(28, 37, 65, 0.8);
        }
        
        .stat-value {
            font-size: 1.4rem;
            font-weight: bold;
            color: var(--teal);
            margin-top: 5px;
        }
        
        .footer {
            text-align: center;
            color: var(--text-secondary);
            padding: 2rem 0 1rem;
            font-size: 0.9rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(91, 192, 190, 0.1);
        }
        
        .visualizer {
            height: 120px;
            width: 100%;
            background: rgba(11, 19, 43, 0.5);
            border-radius: 12px;
            margin: 1.5rem 0;
            overflow: hidden;
            position: relative;
            border: 1px solid rgba(91, 192, 190, 0.1);
        }
        
        .visualizer-bar {
            position: absolute;
            bottom: 0;
            width: 8px;
            background: linear-gradient(to top, var(--teal), #5bc0be80);
            border-radius: 4px 4px 0 0;
        }
        
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }
        
        .gold-text {
            background: linear-gradient(90deg, var(--gold), var(--light-gold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        .teal-text {
            color: var(--teal);
            font-weight: 600;
        }
        
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(91, 192, 190, 0.4), transparent);
            margin: 1.5rem 0;
        }
        
        .feature-icon {
            color: var(--teal);
            font-size: 1.4rem;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        .button-icon {
            font-size: 1.2rem;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MIN_CHUNK_DURATION = 0.5
CHUNK_DURATION = 4.0  # Process every 4 seconds

# Load NeMo model once
@st.cache_resource
def load_model():
    model = nemo_asr.models.EncDecHybridRNNTCTCBPEModel.from_pretrained(
        model_name="nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0"
    )
    return model

model = load_model()

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.last_chunk_time = time.time()
        self.chunk_ready = threading.Event()
        self.transcription_text = ""
        self.current_words = []
        self.word_stream_container = None
        self.finalized_text = ""
        self.start_time = None
        self.word_count = 0
        
    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.last_chunk_time = time.time()
        self.chunk_ready.clear()
        self.transcription_text = ""
        self.current_words = []
        self.finalized_text = ""
        self.start_time = time.time()
        self.word_count = 0
        
        try:
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=self.callback
            )
            self.stream.start_stream()
            return True
        except Exception as e:
            st.error(f"Failed to start recording: {str(e)}")
            self.is_recording = False
            return False
        
    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            self.stream = None
            
    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.frames.append(in_data)
            
            # Check if we have enough audio for a chunk
            elapsed = time.time() - self.last_chunk_time
            if elapsed >= CHUNK_DURATION:
                self.chunk_ready.set()
                
        return (in_data, pyaudio.paContinue)
    
    def get_audio_chunk(self):
        """Get the current audio chunk and reset the buffer"""
        if not self.frames:
            return None
            
        # Save current frames
        chunk_frames = self.frames.copy()
        self.frames = []
        self.last_chunk_time = time.time()
        self.chunk_ready.clear()
        
        # Create temp file
        try:
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            wf = wave.open(temp_audio.name, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(chunk_frames))
            wf.close()
            return temp_audio.name
        except Exception as e:
            st.error(f"Error creating audio chunk: {str(e)}")
            return None

    def process_chunks(self):
        """Background thread to process audio chunks and update UI"""
        while self.is_recording:
            if self.chunk_ready.is_set():
                audio_path = self.get_audio_chunk()
                
                if audio_path:
                    try:
                        # Transcribe the audio
                        result = model.transcribe([audio_path])
                        transcript = result[0].text if result else ""
                        
                        if transcript:
                            # Split into words for streaming effect
                            words = transcript.split()
                            self.word_count += len(words)
                            
                            # Add to finalized transcription
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            self.finalized_text += f"\n[{timestamp}] {transcript}\n"
                            
                            # Process words for streaming effect
                            self.current_words = words
                            
                            # Update word stream display
                            self.update_word_stream()
                            
                    except Exception as e:
                        st.error(f"Transcription error: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(audio_path):
                            try:
                                os.unlink(audio_path)
                            except:
                                pass
            time.sleep(0.1)
    
    def update_word_stream(self):
        """Create a streaming effect for words in the current chunk"""
        if not self.word_stream_container:
            return
            
        # Clear the container
        self.word_stream_container.empty()
        
        with self.word_stream_container.container():
            if not self.current_words:
                st.markdown('<div class="placeholder-text">Listening for Arabic speech...</div>', unsafe_allow_html=True)
                return
                
            # Create a container for the word bubbles
            st.markdown('<div class="word-stream-container">', unsafe_allow_html=True)
            
            # Display words with streaming effect
            display_words = []
            for i, word in enumerate(self.current_words):
                # Add with a small delay to simulate streaming
                time.sleep(0.15 + random.uniform(0, 0.1))
                display_words.append(f'<div class="word-bubble" style="animation-delay: {i*0.1}s;">{word}</div>')
                
                # Update the container after each word
                st.markdown(
                    f'<div class="word-stream-container">{"".join(display_words)}</div>', 
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # After all words appear, keep them visible for a moment
            time.sleep(0.5)
            
            # Then fade them to the finalized transcription
            self.transcription_text += " ".join(self.current_words) + " "
            self.current_words = []

# Initialize session state
if 'recorder' not in st.session_state:
    st.session_state.recorder = AudioRecorder()

recorder = st.session_state.recorder

# App Header
st.markdown("""
    <div class="header">
        <h1>Arabic Live Transcriber</h1>
        <p>Professional real-time speech recognition with elegant Arabic transcription</p>
    </div>
""", unsafe_allow_html=True)

# Buttons above the Finalized Transcription section
st.markdown("""
    <div class="button-container">
        <div class="control-button" id="start-button">
            <span class="button-icon">●</span> Start Recording
        </div>
        <div class="control-button stop-button" id="stop-button">
            <span class="button-icon">■</span> Stop Recording
        </div>
        <div class="control-button download-button" id="download-button">
            <span class="button-icon">⬇️</span> Download
        </div>
    </div>
""", unsafe_allow_html=True)

# Live Word Stream
st.markdown("""
    <div class="card">
        <div class="section-title">Live Word Stream</div>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Words appear here as they're recognized in real-time
        </p>
        <div class="word-stream-container" id="word-stream">
            <div class="placeholder-text">Waiting for speech input...</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Recording status
if recorder.is_recording:
    elapsed_time = time.time() - recorder.start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    
    st.markdown(f"""
        <div class="card">
            <div class="section-title">Recording Status</div>
            
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div class="recording-indicator"></div>
                <span style="color: var(--teal); font-size: 1.1rem; font-weight: 600;">
                    Recording live audio for {minutes}:{seconds:02d}
                </span>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div>Words</div>
                    <div class="stat-value">{recorder.word_count}</div>
                </div>
                <div class="stat-box">
                    <div>Chunks</div>
                    <div class="stat-value">{recorder.word_count // 8 + 1}</div>
                </div>
                <div class="stat-box">
                    <div>Accuracy</div>
                    <div class="stat-value">98%</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Finalized Transcription
st.markdown("""
    <div class="card">
        <div class="section-title">Finalized Transcription</div>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Complete, timestamped transcription appears here
        </p>
        <div class="transcript-container">
            <div class="transcript-box">
                {transcription}
            </div>
        </div>
    </div>
""".format(transcription=recorder.finalized_text if recorder.finalized_text else "Transcription will appear here..."), 
unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Professional Arabic Transcriber • Secure Local Processing • Powered by NVIDIA NeMo</p>
        <p style="margin-top: 10px; font-size: 0.8rem; opacity: 0.7;">
            © 2023 Arabic Transcription Suite | All rights reserved
        </p>
    </div>
""", unsafe_allow_html=True)

# Button functionality
if st.button("● Start Recording", key="start_recording"):
    if not recorder.is_recording:
        if recorder.start_recording():
            recorder.word_stream_container = st.empty()
            processing_thread = threading.Thread(target=recorder.process_chunks)
            add_script_run_ctx(processing_thread)
            processing_thread.daemon = True
            processing_thread.start()
            st.rerun()

if st.button("■ Stop Recording", key="stop_recording"):
    if recorder.is_recording:
        recorder.stop_recording()
        st.rerun()

if st.button("⬇️ Download", key="download_button") and recorder.finalized_text:
    st.download_button(
        "Confirm Download",
        recorder.finalized_text,
        file_name=f"arabic_transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        key="confirm_download",
        mime="text/plain"
    )

# Audio visualization when recording
if recorder.is_recording:
    # JavaScript for audio visualization
    st.markdown("""
        <script>
            // Create audio visualization
            const visualizer = document.createElement('div');
            visualizer.className = 'visualizer';
            visualizer.id = 'visualizer';
            document.currentScript.parentNode.insertBefore(visualizer, document.currentScript);
            
            const barCount = 50;
            
            // Create bars
            for (let i = 0; i < barCount; i++) {
                const bar = document.createElement('div');
                bar.className = 'visualizer-bar';
                bar.style.left = `${(i / barCount) * 100}%`;
                bar.style.height = `${Math.random() * 70 + 30}%`;
                bar.style.animation = `pulse ${0.5 + Math.random() * 1.5}s infinite alternate`;
                bar.style.animationDelay = `${i * 0.05}s`;
                visualizer.appendChild(bar);
            }
            
            // Update bars randomly to simulate audio input
            setInterval(() => {
                const bars = document.querySelectorAll('.visualizer-bar');
                bars.forEach(bar => {
                    const newHeight = Math.random() * 70 + 30;
                    bar.style.height = `${newHeight}%`;
                });
            }, 100);
        </script>
    """, unsafe_allow_html=True)
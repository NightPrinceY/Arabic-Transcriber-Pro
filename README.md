---
title:  Arabic Transcriber Pro
emoji: 🗣️
colorFrom: green
colorTo: red
sdk: streamlit
sdk_version: 1.48.0
app_file: app.py
pinned: true
---
# 🎙️ Arabic Transcriber Pro

> **Convert Arabic speech to text with precision — powered by NVIDIA NeMo and Streamlit.**  
> ✨ Live Demo: [https://huggingface.co/spaces/NightPrince/Arabic-ASR](https://huggingface.co/spaces/NightPrince/Arabic-ASR)  
> 🔗 Portfolio: [https://nightprincey.github.io/Portfolio/](https://nightprincey.github.io/Portfolio/)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-1.28.0+-orange?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/NVIDIA%20NeMo-ASR%20Model-blueviolet?style=for-the-badge&logo=nvidia" />
  <img src="https://img.shields.io/badge/Hugging%20Face-Spaces-FF4B4B?style=for-the-badge&logo=huggingface" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</div>

<br />

![App Screenshot](https://via.placeholder.com/1200x800/0b132b/5bc0be?text=Arabic+Transcriber+Pro)  
*Screenshot: Gloomy-elegant UI with real-time transcription and audio visualization*

---

## 🌟 Overview

**Arabic Transcriber Pro** is a sleek, AI-powered web application that converts spoken **Arabic audio** into accurate, readable text using **NVIDIA’s state-of-the-art NeMo ASR model**. Designed with a modern, **gloomy-elegant aesthetic**, this tool delivers fast, reliable transcription for podcasts, interviews, lectures, and more — all within a user-friendly Streamlit interface hosted on **Hugging Face Spaces**.

Built by **Yahya Alnwsany** — AI Engineer, NLP Specialist, and Hugging Face Ambassador — this project reflects a deep commitment to advancing Arabic NLP and making AI accessible for real-world applications.

🔗 **Live Demo**: [https://huggingface.co/spaces/NightPrince/Arabic-ASR](https://huggingface.co/spaces/NightPrince/Arabic-ASR)  
👤 **Developer Portfolio**: [https://nightprincey.github.io/Portfolio/](https://nightprincey.github.io/Portfolio/)

---

## 🔧 Features

- ✅ **High-Accuracy Arabic ASR** using `nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0`
- 🎧 **Multi-Format Support**: WAV, MP3, OGG, FLAC, M4A
- 🔄 **Auto Audio Conversion**: Resamples to 16kHz mono WAV for optimal model input
- ⚡ **Fast Processing** with real-time progress feedback
- 💾 **Downloadable Transcripts** in `.txt` format
- 🌐 **Web-Based UI** with Streamlit — no installation needed
- 🎨 **Elegant Dark Theme** with RTL-ready Arabic text rendering
- 📊 **Audio Metadata Display**: Duration, sample rate, channels
- 🚀 **Cached Model Loading** for improved performance

---

## 🖼️ UI Design Highlights

- **Color Palette**: Deep navy (`#0b132b`, `#1c2541`) with teal (`#5bc0be`) and coral (`#e55934`) accents
- **Typography**: Clean, modern sans-serif with RTL support
- **Interactive Elements**: Smooth progress bars, hover effects, and responsive layout
- **Responsive Cards & Gradient Headers** for professional feel

---

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|----------|
| Frontend         | [Streamlit](https://streamlit.io) |
| ASR Engine       | [NVIDIA NeMo](https://github.com/NVIDIA/NeMo) |
| Audio Processing | `pydub`, `soundfile` |
| Styling          | Custom CSS (Dark Theme, RTL Support) |
| Hosting          | [Hugging Face Spaces](https://huggingface.co/spaces) |
| Deployment       | Docker / Streamlit / Git |

---

## ▶️ Try It Live

Visit the live app on Hugging Face:

👉 [https://huggingface.co/spaces/NightPrince/Arabic-ASR](https://huggingface.co/spaces/NightPrince/Arabic-ASR)

No setup required — just upload an Arabic audio file and get instant transcription.

---

## 📦 Project Structure
```python
Arabic-transcriber-pro/
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # This file
```

---

## 📂 Supported Audio Formats

| Format | Extension | Notes |
|-------|----------|-------|
| WAV   | `.wav`   | Native support |
| MP3   | `.mp3`   | Requires `ffmpeg` |
| OGG   | `.ogg`   | Vorbis/Opus |
| FLAC  | `.flac`  | Lossless |
| M4A   | `.m4a`   | AAC audio |

> 🔁 All files are automatically converted to **16kHz mono WAV** before transcription.

---

## About the Developer

### 👤 [Yahya Alnwsany](https://nightprincey.github.io/Portfolio/)
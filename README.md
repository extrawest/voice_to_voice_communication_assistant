# 🎙️ Voice-to-Voice Communication Assistant

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Maintainer](https://img.shields.io/static/v1?label=Yevhen%20Ruban&message=Maintainer&color=red)](mailto:yevhen.ruban@extrawest.com)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

A scalable voice assistant implementation using LiveKit for real-time communication, with custom Speech-to-Text (STT) and Text-to-Speech (TTS) integrations using local APIs.



https://github.com/user-attachments/assets/0e8ccc11-c21f-4d22-9904-eccede307123



## 🚀 Features

- **🗣️ Voice-to-Voice Communication**: Real-time voice interaction with an AI assistant
- **🔌 Local API Integration**: Uses local APIs for STT, TTS, and LLM processing
  - Custom STT using local Speeches AI API
  - Custom TTS using local Kokoro AI API
  - Integration with Ollama for local LLM processing
- **🛠️ Additional Tools**:
  - 🔍 Web search capability using Tavily API
  - 🌤️ Weather information retrieval
- **🔄 LiveKit Integration**: Leverages LiveKit's powerful real-time communication framework
- **🎤 Voice Activity Detection**: Uses Silero VAD for accurate speech detection
- **🔇 Noise Cancellation**: Integrated noise reduction for better audio quality

## 📋 Prerequisites

- Python 3.10+
- LiveKit server (local or cloud)
- Local STT API (Speeches AI)
- Local TTS API (Kokoro AI)
- Ollama running locally

## 💻 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/extrawest/voice_to_voice_communication_assistant.git
   cd voice_to_voice_communication_assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by copying the example file:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your configuration:
   ```
   # LiveKit Configuration
   LIVEKIT_URL=ws://localhost:7880
   LIVEKIT_API_KEY=devkey
   LIVEKIT_API_SECRET=secret

   # STT Configuration
   STT_API_URL=your_url

   # LLM Configuration
   LLM_API_URL=your_url

   # TTS Configuration
   TTS_API_URL=your_url
   TTS_API_KEY=your-api-key

   # Optional API Keys for Additional Features
   WEATHER_API_KEY=your-weather-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ```

## 🚀 Running the Application

### Backend Setup

1. Run the voice assistant backend:
   ```bash
   python main.py dev
   ```

### Frontend Setup

1. Clone the LiveKit voice assistant frontend repository:
   ```bash
   git clone https://github.com/livekit-examples/voice-assistant-frontend
   cd voice-assistant-frontend
   ```

2. Install dependencies and start the frontend:
   ```bash
   npm install
   npm run dev
   ```

3. Open your browser and navigate to http://localhost:3000

4. Start interacting with your voice assistant!

## 🏗️ Architecture

The application consists of several key components:

![Architecture Diagram](https://mermaid.ink/img/pako:eNp1kk1PwzAMhv9KlBMgdT3QA4deEEJiQmicJg5VG9M6tHFVJ9UK7b-T9mOlMHGK_T7PK8dZHrRFyXnpWtQOXlCZo0bVQW3QgbKwQVNBZQ1Uh1rBGvUOKgRrLTkMVhsXYI_WoYEXVB0qgzXVIEONDmwNO3QWFG4DKKqtQRlgj3uEV-3I5RO8aUdlEBTUxkKHDRTGNh3UgWw-wVk0sEKDJhA8aEtVnmGnHdFCYbQJRJMHWKKhDgJZKFzQJRrXQxHI5gPMUPXaOWgCwSNqS1We4QlVQ7QQyOYDvGlDdgLBHVpHVZ7hGVVLtBDI5gO8GHQmEDygdVTlGc7QdEQLgWw-wBKNDgQP2jmq8gxrNB3RQiCbD_DJHwkEj9o5qvIMG-06ooVANv_DGxpLr3CC1lGVZ9hq1xItBLL5AO_aUJVA8KSdoyrP8KJdR7QQyOYDfNKvCQRP2lmq8gxb7TqihUA2H-ATDf2aQPBZO0tVnmGvXUe0EMjmA3zQrwkEz9pZqvIMB-06ooVANv_DK5qefk0geNHOUpVnOGrXES0EsvkA_-SvCQTP2lmq8gxH7TqihUA2H-CdXk0gWGjnqMozfNWuJVoIZPMBPtBQlUBwp52jKs_wTbuWaCGQzQf4i35NIHjVzlGVZzhp1xItBLL5AO_0awLBQjtLVZ7hpF1HtBDI5gMc6NcEgmftLFV5hm_atUQLgWw-wLEPgeBFO0dVnuGkXUu0EMjmA-z71wSChXaWqjzDSbuOaCGQzQc49K8JBM_aWaraf_8AYdAm0Q?type=png)

- **LiveKit Integration**: Handles real-time audio streaming and room management
- **Custom STT Class**: Processes audio input and converts it to text
- **Custom TTS Class**: Converts text responses to speech
- **Ollama LLM Integration**: Processes text input and generates responses
- **Agent Implementation**: Manages the conversation flow and tools

Developed by [extrawest](https://extrawest.com/). Software development company

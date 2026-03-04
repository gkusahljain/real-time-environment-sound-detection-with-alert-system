# IntelliSound: Real-Time Environment Sound Detection with Alert System 🎧🚨

IntelliSound is an advanced, AI-driven audio surveillance and safety monitoring system. It leverages state-of-the-art **PANNs (Pretrained Audio Neural Networks)** to identify environmental sounds in real-time, providing immediate visual feedback and SMS alerts via **Twilio** for critical events like gunshots, sirens, or fire alarms.

---

## ✨ Features

- 🔊 **Real-time Monitoring**: Continuous audio capture and analysis directly from the browser's microphone.
- 🤖 **Deep Learning Inference**: Uses high-performance audio tagging models trained on 5000+ hours of data (AudioSet).
- 🚨 **Smart Alert System**: Automatically detects critical sounds (Gunshot, Siren, Fire Alarm) and sends SMS notifications via Twilio.
- 📊 **Visual Feedback**:
  - Live confidence progress bars for detected sounds.
  - Dynamic **Mel-Spectrogram** generation for acoustic analysis.
- 🗄️ **Event Logging**: Every sound detected is logged to a local SQLite database for historical review.
- 🔥 **Modern UI**: A premium, responsive "glassmorphism" web application frontend.

---

## 🛠 Tech Stack

- **Backend**: Python, Flask, PANNs (via `panns_inference`), FFmpeg, SQLite, Twilio API.
- **Frontend**: Vanilla HTML5, CSS3 (Modern UI), JavaScript (Speech-to-Text, MediaRecorder API).
- **Core AI**: PyTorch, Librosa (Audio Processing).

---

## 🚀 Getting Started

### 📦 Prerequisites

1.  **Python 3.7+**
2.  **FFmpeg**: Required for audio format conversion.
    ```bash
    # Windows (using Chocolatey)
    choco install ffmpeg
    
    # Linux (Ubuntu/Debian)
    sudo apt install ffmpeg
    ```
3.  **Twilio Account**: To enable the SMS alert system.

### 🍱 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/gkusahljain/real-time-environment-sound-detection-with-alert-system.git
    cd real-time-environment-sound-detection-with-alert-system
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install panns_inference
    ```

3.  **Configure API Keys**:
    Edit `backend/alert_engine.py` with your Twilio credentials:
    ```python
    ACCOUNT_SID = "your_sid"
    AUTH_TOKEN = "your_token"
    FROM_NUMBER = "your_twilio_number"
    TO_NUMBER = "your_emergency_contact"
    ```

---

## 🖥 Usage

### ⚙️ Running the Backend
```bash
cd backend
python app.py
```
The Flask server will start on `http://127.0.0.1:8000`.

### 🌐 Running the Frontend
Simply open `frontend/index.html` in any modern browser or use a Live Server.

### 🎙 Monitoring
1.  Click **"▶ Start Monitoring"** to allow microphone access.
2.  The system will analyze audio in 2-second chunks.
3.  Detected sounds and alerts will appear instantly on the dashboard.

---

## 📝 Project Architecture

The system follows a modular architecture:
1.  **Capture**: Frontend records audio chunks using `MediaRecorder`.
2.  **Convert**: Backend uses `FFmpeg` to transcode chunks to `.wav`.
3.  **Inference**: PANNs processes the audio and outputs classification labels and scores.
4.  **Action**: 
    - Log results to `events.db`.
    - If a sound matches the "Critical List" (defined in `config.py`), an SMS is dispatched.
5.  **Visualize**: Results and a Mel-spectrogram are pushed back to the UI.

---

## 📸 Screenshots

![IntelliSound Dashboard](https://raw.githubusercontent.com/gkusahljain/real-time-environment-sound-detection-with-alert-system/main/485dcac3-54db-4fbe-af37-d4ddcfc4a374.png)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE.MIT).

## 🤝 Acknowledgements

Special thanks to [Qiuqiang Kong](https://github.com/qiuqiangkong) for the PANNs codebase and to the AudioSet researchers.

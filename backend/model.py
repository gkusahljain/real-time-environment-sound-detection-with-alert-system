import librosa
import torch
from panns_inference import AudioTagging, labels

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", DEVICE)

model = AudioTagging(device=DEVICE)

def analyze_audio(path):
    audio, _ = librosa.load(path, sr=32000, mono=True)
    audio = audio[None, :]

    output, _ = model.inference(audio)
    probs = output[0]

    results = []
    for i, p in enumerate(probs):
        if p > 0.1:
            results.append({
                "label": labels[i],
                "score": round(float(p), 3)
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import librosa.display

def generate_spectrogram(path):
    try:
        y, sr = librosa.load(path, sr=32000)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        return None

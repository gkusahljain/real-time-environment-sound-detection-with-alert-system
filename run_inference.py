import librosa
from panns_inference import AudioTagging, labels

print("Loading audio...")

audio_path = "audio_samples/hi.wav"
audio, sr = librosa.load(audio_path, sr=32000, mono=True)
audio = audio[None, :]

print("Audio loaded. Running model...")

at = AudioTagging(device="cpu")

clipwise_output, _ = at.inference(audio)

print("\n=== Top 5 Predicted Sound Tags ===")

probs = clipwise_output[0]
top_indices = probs.argsort()[-5:][::-1]

for idx in top_indices:
    print(f"{labels[idx]}: {probs[idx]:.3f}")

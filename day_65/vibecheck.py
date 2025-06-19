import sounddevice as sd
import numpy as np
import librosa
import joblib
import time
import os

# Emotion labels (adjust based on your model training)
emotion_labels = ['neutral', 'happy', 'sad', 'angry']

# Function to record audio
def record_audio(duration=5, fs=22050):
    print("Recording... Speak now! (5 seconds)")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished!")
    return audio[:, 0]

# Function to extract MFCC features
def extract_features(audio, fs=22050):
    mfccs = librosa.feature.mfcc(y=audio, sr=fs, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Function to predict emotion (placeholder if no model)
def predict_emotion(features):
    if 'model' not in globals() or model is None:
        return "Emotion detection unavailable (no model loaded)"
    features = features.reshape(1, -1)  # Reshape for model input
    prediction = model.predict(features)
    return emotion_labels[prediction[0]]

# Main loop for real-time emotion detection
def vibe_check():
    global model
    # Check for model file
    if not os.path.exists('emotion_model.joblib'):
        print("Warning: 'emotion_model.joblib' not found. Emotion detection will be unavailable.")
        print("Please train a model using the RAVDESS dataset or download a pretrained one.")
        print("For now, the script will run but return a placeholder response.")
        model = None
    else:
        model = joblib.load('emotion_model.joblib')

    print("Welcome to VibeCheck! Press Ctrl+C to exit.")
    while True:
        try:
            # Record 5 seconds of audio
            audio = record_audio()
            
            # Extract features
            features = extract_features(audio)
            
            # Predict emotion
            emotion = predict_emotion(features)
            
            # Provide feedback
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S %Z")
            print(f"[Time: {timestamp}] Detected emotion: {emotion}!")
            print("--------------------------------")
            
            time.sleep(1)  # Small delay before next recording
            
        except KeyboardInterrupt:
            print("\nThanks for using VibeCheck! Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)

if __name__ == "__main__":
    vibe_check()
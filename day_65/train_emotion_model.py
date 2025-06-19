import os
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Adjust these labels based on your needs
emotion_map = {
    '01': 'neutral',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry'
}

def extract_features(file_path):
    audio, sr = librosa.load(file_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

def get_emotion_from_filename(filename):
    # RAVDESS: filename format = '03-01-05-01-02-01-12.wav'
    emotion_code = filename.split('-')[2]
    return emotion_map.get(emotion_code)

data = []
labels = []

# Change this to your extracted RAVDESS folder path
ravdess_path = r'C:\Users\uday kumar\Downloads\Audio_Speech_Actors_01-24'

for root, _, files in os.walk(ravdess_path):
    for file in files:
        if file.endswith('.wav'):
            emotion = get_emotion_from_filename(file)
            if emotion:
                try:
                    features = extract_features(os.path.join(root, file))
                    data.append(features)
                    labels.append(list(emotion_map.values()).index(emotion))
                except Exception as e:
                    print(f"Error processing {file}: {e}")

X = np.array(data)
y = np.array(labels)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=list(emotion_map.values())))

# Save model
joblib.dump(clf, 'emotion_model.joblib')
print("Model saved as emotion_model.joblib")
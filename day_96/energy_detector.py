import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import io
import streamlit as st
import os

class EnergyDetector:
    def __init__(self):
        self.energy_mapping = {
            'happy': 'High',
            'surprise': 'High', 
            'neutral': 'Medium',
            'sad': 'Low',
            'angry': 'Low',
            'fear': 'Low',
            'disgust': 'Low'
        }
        
        # Fallback energy levels based on facial features
        self.fallback_indicators = {
            'eyes_open': 'High',
            'slight_smile': 'Medium', 
            'neutral_expression': 'Medium',
            'tired_eyes': 'Low',
            'frown': 'Low'
        }
    
    def detect_energy(self, image_input):
        """
        Detect energy level from image with realistic expectations
        Returns: (energy_level, confidence)
        """
        try:
            # Convert image input to format DeepFace can process
            if hasattr(image_input, 'read'):
                # Streamlit uploaded file
                image_bytes = image_input.read()
                image_input.seek(0)  # Reset file pointer
            else:
                # Camera input
                image_bytes = image_input.getvalue()
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Try DeepFace emotion detection
            try:
                result = DeepFace.analyze(
                    opencv_image, 
                    actions=['emotion'],
                    enforce_detection=False,
                    detector_backend='opencv'
                )
                
                if isinstance(result, list):
                    result = result[0]
                
                # Get dominant emotion
                emotions = result['emotion']
                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]
                
                # Map emotion to energy level
                energy_level = self.energy_mapping.get(dominant_emotion, 'Medium')
                
                # Adjust confidence based on emotion strength
                if confidence > 70:
                    confidence = min(confidence, 95)  # Cap at 95% for realism
                else:
                    confidence = max(confidence, 30)  # Minimum 30% confidence
                
                return energy_level, confidence
                
            except Exception as e:
                st.warning(f"DeepFace analysis failed: {str(e)}")
                return self._fallback_analysis(opencv_image)
                
        except Exception as e:
            st.error(f"Image processing error: {str(e)}")
            return "Medium", 50.0
    
    def _fallback_analysis(self, image):
        """
        Fallback analysis using basic OpenCV features
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            try:
                haarcascades_path = getattr(cv2, 'data', None)
                if haarcascades_path:
                    face_cascade = cv2.CascadeClassifier(haarcascades_path.haarcascades + 'haarcascade_frontalface_default.xml')
                    eye_cascade = cv2.CascadeClassifier(haarcascades_path.haarcascades + 'haarcascade_eye.xml')
                else:
                    return "Medium", 40.0
            except Exception:
                return "Medium", 40.0
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return "Medium", 30.0
            
            # Analyze first face
            x, y, w, h = faces[0]
            roi_gray = gray[y:y+h, x:x+w]
            
            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            # Simple heuristics
            if len(eyes) >= 2:
                # Eyes detected - likely alert/engaged
                return "High", 60.0
            else:
                # No eyes detected - could be tired or poor lighting
                return "Medium", 40.0
                
        except Exception as e:
            return "Medium", 30.0
    
    def get_energy_description(self, energy_level):
        """
        Get human-readable description of energy level
        """
        descriptions = {
            'High': 'Alert, focused, and energized',
            'Medium': 'Balanced and steady',
            'Low': 'Tired or needing rest'
        }
        return descriptions.get(energy_level, 'Unknown')
    
    def get_productivity_tip(self, energy_level):
        """
        Get productivity tip based on energy level
        """
        tips = {
            'High': 'Perfect time for creative work and important decisions!',
            'Medium': 'Good for routine tasks and meetings',
            'Low': 'Consider taking a break or doing lighter tasks'
        }
        return tips.get(energy_level, 'Focus on what feels right for you') 
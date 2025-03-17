from transformers import pipeline
import csv
import os
from datetime import datetime
import streamlit as st
# Initialize emotion detection pipeline from Hugging Face


# CSV file to store logs
CSV_FILE = "prompts.csv"

# Ensure the CSV file exists with headers
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Prompt", "Detected Emotion"])  # Headers

# Function to log detected emotions
def log_emotion(prompt, emotion):
    initialize_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prompt, emotion])

# Function to detect emotion from transcribed text
@st.cache_data()
def detect_emotion(text):
    """Function to detect emotion from transcribed text."""
    # Get emotion classification
    emotion_recognizer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    result = emotion_recognizer(text)
    emotion = result[0]['label']

    # Log the detected emotion
    log_emotion(text, emotion)

    return emotion

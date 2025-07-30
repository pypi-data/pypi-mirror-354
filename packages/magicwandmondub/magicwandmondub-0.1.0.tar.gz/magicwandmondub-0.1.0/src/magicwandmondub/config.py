from google.cloud import speech
from dotenv import load_dotenv
import os

# --- Audio Recording Settings ---
DEFAULT_CHANNELS = 1
SAMPLE_RATE = 16000

CHUNK_DURATION_S = 0.5  # Duration of each audio chunk in seconds
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_S)  # Number of samples per chunk

OUTPUT_DIR = "recordings"
AUDIO_EXTENSION = ".wav"
AUDIO_ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16

# --- UI Settings ---
# Initial window dimensions for the application
INITIAL_WINDOW_GEOMETRY = "500x200"
# Window dimensions for the recording page
RECORDING_WINDOW_GEOMETRY = "400x250"
# Flag to enable/disable window resizing
RESIZABLE_WINDOW = False


# Speech-to-Text Configuration
# Default language code for speech recognition (BCP-47 format)
DEFAULT_LANGUAGE_CODE = "mn-MN"  # Mongolian language code
load_dotenv()
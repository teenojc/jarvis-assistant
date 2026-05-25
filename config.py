import os
from dotenv import load_dotenv

load_dotenv()

# Voice Configuration
VOICE_CONFIG = {
    'language': 'en-US',
    'microphone_index': None,  # Auto-detect
    'timeout': 10,
    'phrase_time_limit': 30,
    'energy_threshold': 4000,
}

# Text-to-Speech Configuration
TTS_CONFIG = {
    'rate': 150,  # Speed of speech
    'volume': 0.9,  # Volume level
    'voice_gender': 'male',  # 'male' or 'female'
}

# NLP Configuration
NLP_CONFIG = {
    'model_name': 'en_core_web_sm',  # spaCy model
    'intent_model': 'distilbert-base-uncased-finetuned-sst-2-english',
    'confidence_threshold': 0.7,
}

# Task Automation Configuration
TASK_CONFIG = {
    'enable_scheduler': True,
    'timezone': 'UTC',
}

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': 'jarvis.log',
}

# Assistant Configuration
ASSISTANT_CONFIG = {
    'name': 'JARVIS',
    'personality': 'formal',  # 'formal', 'casual', 'witty'
    'response_timeout': 5,
    'debug_mode': False,
}
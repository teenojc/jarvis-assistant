"""Text-to-Speech Module"""

import pyttsx3
from loguru import logger
from config import TTS_CONFIG


class TextToSpeech:
    """Handle text-to-speech conversion"""
    
    def __init__(self):
        """Initialize text-to-speech engine"""
        self.engine = pyttsx3.init()
        
        # Configure engine
        self.engine.setProperty('rate', TTS_CONFIG['rate'])
        self.engine.setProperty('volume', TTS_CONFIG['volume'])
        
        # Set voice gender
        voices = self.engine.getProperty('voices')
        if TTS_CONFIG['voice_gender'].lower() == 'female':
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        else:
            self.engine.setProperty('voice', voices[0].id)
        
        logger.info("Text-to-Speech engine initialized")
    
    def speak(self, text):
        """Speak the given text"""
        logger.info(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Error during speech: {e}")
            return False
    
    def speak_async(self, text):
        """Speak asynchronously (non-blocking)"""
        logger.info(f"Speaking (async): {text}")
        try:
            self.engine.say(text)
            # Don't wait for completion
            return True
        except Exception as e:
            logger.error(f"Error during async speech: {e}")
            return False
    
    def save_to_file(self, text, filename):
        """Save speech to audio file"""
        logger.info(f"Saving speech to file: {filename}")
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            logger.info(f"Speech saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            return False
    
    def set_rate(self, rate):
        """Set speech rate"""
        self.engine.setProperty('rate', rate)
        logger.info(f"Speech rate set to {rate}")
    
    def set_volume(self, volume):
        """Set speech volume"""
        self.engine.setProperty('volume', min(1.0, max(0.0, volume)))
        logger.info(f"Speech volume set to {volume}")
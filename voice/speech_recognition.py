"""Speech Recognition Module"""

import speech_recognition as sr
from loguru import logger
from config import VOICE_CONFIG


class SpeechRecognizer:
    """Handle speech-to-text conversion"""
    
    def __init__(self):
        """Initialize speech recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Set energy threshold for ambient noise
        self.recognizer.energy_threshold = VOICE_CONFIG['energy_threshold']
        
        logger.info("Speech Recognizer initialized")
    
    def calibrate_microphone(self, duration=2):
        """Calibrate microphone for ambient noise"""
        logger.info(f"Calibrating microphone for {duration} seconds...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=duration
                )
            logger.info("Microphone calibrated")
            return True
        except Exception as e:
            logger.error(f"Microphone calibration failed: {e}")
            return False
    
    def recognize(self):
        """Recognize speech from microphone"""
        try:
            with self.microphone as source:
                logger.info("Listening...")
                
                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_CONFIG['timeout'],
                    phrase_time_limit=VOICE_CONFIG['phrase_time_limit']
                )
            
            logger.info("Processing audio...")
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(
                    audio,
                    language=VOICE_CONFIG['language']
                )
                logger.info(f"Recognized: {text}")
                return text
            
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            
            except sr.RequestError as e:
                logger.error(f"Google Speech Recognition service error: {e}")
                return None
        
        except sr.RequestError as e:
            logger.error(f"Could not request results: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error during speech recognition: {e}")
            return None
    
    def recognize_from_file(self, audio_file):
        """Recognize speech from audio file"""
        logger.info(f"Recognizing speech from file: {audio_file}")
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(
                audio,
                language=VOICE_CONFIG['language']
            )
            logger.info(f"Recognized: {text}")
            return text
        
        except Exception as e:
            logger.error(f"Error recognizing from file: {e}")
            return None
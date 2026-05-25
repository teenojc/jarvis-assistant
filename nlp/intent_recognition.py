"""Intent Recognition Module"""

from loguru import logger
from transformers import pipeline
from config import NLP_CONFIG


class IntentRecognizer:
    """Recognize user intent from text"""
    
    def __init__(self):
        """Initialize intent recognizer"""
        logger.info("Initializing Intent Recognizer...")
        
        # Load zero-shot classification model
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Define possible intents
        self.intents = [
            'greeting',
            'time',
            'weather',
            'task',
            'reminder',
            'help',
            'information',
            'control',
        ]
        
        logger.info("Intent Recognizer initialized")
    
    def recognize(self, text):
        """Recognize intent from text"""
        logger.info(f"Recognizing intent from: {text}")
        
        try:
            result = self.classifier(
                text,
                self.intents,
                multi_class=False
            )
            
            intent = result['labels'][0]
            confidence = result['scores'][0]
            
            logger.info(f"Intent: {intent}, Confidence: {confidence:.2f}")
            
            if confidence >= NLP_CONFIG['confidence_threshold']:
                return intent
            else:
                logger.warning(f"Low confidence for intent recognition: {confidence}")
                return 'unknown'
        
        except Exception as e:
            logger.error(f"Error during intent recognition: {e}")
            return 'unknown'
    
    def get_intent_description(self, intent):
        """Get description of an intent"""
        descriptions = {
            'greeting': 'User is greeting the assistant',
            'time': 'User wants to know the time',
            'weather': 'User wants weather information',
            'task': 'User wants to perform a task',
            'reminder': 'User wants to set a reminder',
            'help': 'User wants help',
            'information': 'User wants general information',
            'control': 'User wants to control something',
        }
        return descriptions.get(intent, 'Unknown intent')
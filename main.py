#!/usr/bin/env python3
"""
JARVIS Assistant - Main Entry Point
A voice-activated AI assistant inspired by Tony Stark's JARVIS
"""

import sys
from loguru import logger
from voice.speech_recognition import SpeechRecognizer
from voice.text_to_speech import TextToSpeech
from nlp.intent_recognition import IntentRecognizer
from nlp.entity_extraction import EntityExtractor
from tasks.automation import TaskAutomation
from config import ASSISTANT_CONFIG, LOGGING_CONFIG

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=LOGGING_CONFIG['level'],
    format=LOGGING_CONFIG['format']
)
logger.add(
    LOGGING_CONFIG['log_file'],
    level=LOGGING_CONFIG['level'],
    format=LOGGING_CONFIG['format']
)


class JARVIS:
    """Main JARVIS Assistant Class"""
    
    def __init__(self):
        """Initialize JARVIS components"""
        logger.info(f"Initializing {ASSISTANT_CONFIG['name']} Assistant...")
        
        self.name = ASSISTANT_CONFIG['name']
        self.personality = ASSISTANT_CONFIG['personality']
        
        # Initialize components
        self.speech_recognizer = SpeechRecognizer()
        self.text_to_speech = TextToSpeech()
        self.intent_recognizer = IntentRecognizer()
        self.entity_extractor = EntityExtractor()
        self.task_automation = TaskAutomation()
        
        self.is_running = False
        logger.info(f"{self.name} initialized successfully")
    
    def greet(self):
        """Greet the user"""
        greeting = f"Good morning, Sir. {self.name} at your service. How may I assist you today?"
        logger.info(f"Greeting: {greeting}")
        self.text_to_speech.speak(greeting)
    
    def listen(self):
        """Listen for user command"""
        logger.info("Listening for command...")
        try:
            command = self.speech_recognizer.recognize()
            if command:
                logger.info(f"Command recognized: {command}")
                self.text_to_speech.speak(f"I heard: {command}")
                return command
        except Exception as e:
            logger.error(f"Error during listening: {e}")
            self.text_to_speech.speak("I didn't catch that. Could you please repeat?")
        return None
    
    def process_command(self, command):
        """Process user command"""
        logger.info(f"Processing command: {command}")
        
        # Extract intent
        intent = self.intent_recognizer.recognize(command)
        logger.info(f"Detected intent: {intent}")
        
        # Extract entities
        entities = self.entity_extractor.extract(command)
        logger.info(f"Extracted entities: {entities}")
        
        # Execute appropriate action
        response = self.execute_action(intent, entities, command)
        
        if response:
            self.text_to_speech.speak(response)
        
        return response
    
    def execute_action(self, intent, entities, command):
        """Execute action based on intent"""
        logger.info(f"Executing action for intent: {intent}")
        
        # Map intents to actions
        intent_map = {
            'greeting': self.handle_greeting,
            'time': self.handle_time,
            'weather': self.handle_weather,
            'task': self.handle_task,
            'reminder': self.handle_reminder,
            'help': self.handle_help,
        }
        
        handler = intent_map.get(intent, self.handle_unknown)
        return handler(command, entities)
    
    def handle_greeting(self, command, entities):
        """Handle greeting intent"""
        return "Good day, Sir. How may I be of service?"
    
    def handle_time(self, command, entities):
        """Handle time query"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}"
    
    def handle_weather(self, command, entities):
        """Handle weather query"""
        return "I'm unable to retrieve weather data at the moment, Sir."
    
    def handle_task(self, command, entities):
        """Handle task automation"""
        return "Task automation feature coming soon, Sir."
    
    def handle_reminder(self, command, entities):
        """Handle reminder setting"""
        return "Reminder set successfully, Sir."
    
    def handle_help(self, command, entities):
        """Handle help request"""
        return "I can help you with time, weather, reminders, and various tasks. What would you like to know?"
    
    def handle_unknown(self, command, entities):
        """Handle unknown intent"""
        return "I'm sorry, Sir. I didn't understand that. Could you please rephrase?"
    
    def run(self):
        """Main JARVIS loop"""
        self.is_running = True
        logger.info(f"{self.name} started")
        
        self.greet()
        
        while self.is_running:
            try:
                # Listen for command
                command = self.listen()
                
                if command:
                    # Check for exit commands
                    if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'shutdown']):
                        self.shutdown()
                        break
                    
                    # Process and respond to command
                    self.process_command(command)
                
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                self.text_to_speech.speak("An error occurred, Sir. Attempting to recover.")
    
    def shutdown(self):
        """Shutdown JARVIS"""
        logger.info(f"Shutting down {self.name}")
        self.text_to_speech.speak("Goodbye, Sir. Until we meet again.")
        self.is_running = False


def main():
    """Main entry point"""
    try:
        jarvis = JARVIS()
        jarvis.run()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
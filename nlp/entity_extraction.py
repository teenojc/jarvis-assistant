"""Entity Extraction Module"""

import spacy
from loguru import logger
from config import NLP_CONFIG


class EntityExtractor:
    """Extract entities from text"""
    
    def __init__(self):
        """Initialize entity extractor"""
        logger.info("Initializing Entity Extractor...")
        
        try:
            self.nlp = spacy.load(NLP_CONFIG['model_name'])
            logger.info(f"Loaded spacy model: {NLP_CONFIG['model_name']}")
        except OSError:
            logger.warning(f"Model {NLP_CONFIG['model_name']} not found. Installing...")
            import os
            os.system(f"python -m spacy download {NLP_CONFIG['model_name']}")
            self.nlp = spacy.load(NLP_CONFIG['model_name'])
        
        logger.info("Entity Extractor initialized")
    
    def extract(self, text):
        """Extract entities from text"""
        logger.info(f"Extracting entities from: {text}")
        
        try:
            doc = self.nlp(text)
            
            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
            
            logger.info(f"Extracted entities: {entities}")
            return entities
        
        except Exception as e:
            logger.error(f"Error during entity extraction: {e}")
            return {}
    
    def extract_person(self, text):
        """Extract person entities"""
        doc = self.nlp(text)
        persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        return persons
    
    def extract_time(self, text):
        """Extract time entities"""
        doc = self.nlp(text)
        times = [ent.text for ent in doc.ents if ent.label_ in ['TIME', 'DATE']]
        return times
    
    def extract_location(self, text):
        """Extract location entities"""
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
        return locations
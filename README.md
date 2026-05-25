# JARVIS Assistant

A voice-activated AI assistant inspired by Tony Stark's JARVIS from Iron Man.

## Features

- 🎤 **Voice Recognition** - Understand spoken commands
- 🧠 **Natural Language Processing** - Comprehend user intent
- 🗣️ **Text-to-Speech** - Respond with synthesized voice
- ⚙️ **Task Automation** - Execute automated tasks
- 🎯 **Intent Recognition** - Identify what the user wants
- 📝 **Entity Extraction** - Extract relevant information

## Tech Stack

- **Language**: Python 3.8+
- **Voice Recognition**: `speech_recognition`
- **Text-to-Speech**: `pyttsx3`
- **NLP**: `spaCy` + `Hugging Face Transformers`
- **Task Scheduling**: `APScheduler`
- **Web Interface**: Flask

## Installation

```bash
git clone https://github.com/teenojc/jarvis-assistant.git
cd jarvis-assistant
pip install -r requirements.txt
```

## Quick Start

```bash
python main.py
```

Then speak to activate JARVIS!

## Project Structure

```
jarvis-assistant/
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── voice/
│   ├── __init__.py
│   ├── speech_recognition.py   # Voice input handler
│   └── text_to_speech.py       # Voice output handler
├── nlp/
│   ├── __init__.py
│   ├── intent_recognition.py   # Intent classifier
│   └── entity_extraction.py    # Entity recognizer
├── tasks/
│   ├── __init__.py
│   ├── automation.py      # Task automation logic
│   └── scheduler.py       # Task scheduling
├── utils/
│   ├── __init__.py
│   └── logger.py          # Logging utilities
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Usage Examples

```
"What time is it?"
"Turn on the lights"
"Set a reminder for 3 PM"
"What's the weather?"
"Play my favorite music"
"Schedule a meeting at 2 PM"
```

## Development

Contributions are welcome! Please follow these steps:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

Tony Stark's Protocol Implementation by @teenojc
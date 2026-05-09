# Zen Bot

Zen Bot is a local-first voice assistant MVP built in Python. It uses modular architecture for easy extension and maintenance.

## Features

- Wake word activation ("zen")
- Real-time speech-to-text using faster-whisper
- Offline text-to-speech using Piper
- Basic command execution (open/close camera, sleep)
- Grok API integration for general queries
- State management (active/sleep modes)
- Logging and configuration

## Requirements

- Python 3.8+
- Microphone access
- GPU recommended for faster-whisper

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Piper TTS model (e.g., en_US-lessac-medium) and place in a models/ directory or update config
4. Set your Grok API key in config.json
5. Run:
   ```bash
   python -m zen_bot.main
   ```

## Architecture

```
zen_bot/
├── main.py          # Main application loop
├── wakeword.py      # Wake word detection
├── stt.py           # Speech-to-text
├── tts.py           # Text-to-speech
├── commands.py      # Predefined commands
├── grok.py          # LLM backend
└── utils/
    └── audio.py     # Audio utilities
```

## Configuration

Edit `config.json` to customize:

- Wake word
- Silence threshold
- Model selections
- API keys

## Usage

1. Say "zen" to activate
2. Bot responds "Yes?"
3. Speak your command or query
4. Bot processes and responds

Predefined commands:

- "open camera" - Opens camera window
- "close camera" - Closes camera
- "sleep" - Puts bot to sleep mode

For other queries, uses Grok API.

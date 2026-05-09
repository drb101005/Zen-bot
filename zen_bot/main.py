import json
import logging
import threading
from zen_bot.wakeword import WakeWordDetector
from zen_bot.stt import STT
from zen_bot.tts import TTS
from zen_bot.commands import open_camera, close_camera, sleep
from zen_bot.grok import GrokAPI
from zen_bot.utils.audio import record_audio, save_audio_to_wav
import os

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ZenBot:
    def __init__(self):
        self.state = "active"  # active or sleep
        self.stt = STT(config['stt_model'])
        self.tts = TTS(config['tts_model_path'])
        self.grok = GrokAPI(config['grok_api_key'], config['grok_url'])
        self.wake_detector = WakeWordDetector(config['wake_word'], self.on_wake_word)

    def start(self):
        logging.info("Starting Zen Bot")
        self.wake_detector.start_listening()
        while self.state == "active":
            pass  # Keep running

    def on_wake_word(self):
        if self.state == "sleep":
            return
        logging.info("Wake word detected")
        self.tts.speak("Yes?")
        # Record user input
        audio, sr = record_audio(silence_duration=config['silence_threshold'])
        audio_file = save_audio_to_wav(audio, sr)
        # Transcribe
        transcription = self.stt.transcribe(audio_file)
        logging.info(f"Transcription: {transcription}")
        os.remove(audio_file)  # Clean up
        # Process
        self.process_input(transcription)

    def process_input(self, text):
        text_lower = text.lower().strip()
        if text_lower == "open camera":
            response = open_camera()
        elif text_lower == "close camera":
            response = close_camera()
        elif text_lower == "sleep":
            response = sleep()
            self.state = "sleep"
        else:
            response = self.grok.get_response(text)
        logging.info(f"Response: {response}")
        self.tts.speak(response)

if __name__ == "__main__":
    bot = ZenBot()
    bot.start()
from piper import PiperVoice
import sounddevice as sd
import numpy as np

class TTS:
    def __init__(self, model_path):
        self.voice = PiperVoice.load(model_path)

    def speak(self, text):
        """
        Synthesize and play text.
        """
        audio = self.voice.synthesize(text)
        # Piper returns audio as numpy array
        sd.play(audio, samplerate=22050)
        sd.wait()
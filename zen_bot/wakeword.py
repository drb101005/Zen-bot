import pocketsphinx as ps
import pyaudio
import threading
import queue

class WakeWordDetector:
    def __init__(self, wake_word="zen", callback=None):
        self.wake_word = wake_word
        self.callback = callback
        self.is_listening = False
        self.audio_queue = queue.Queue()

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False

    def _listen_loop(self):
        # Initialize pocketsphinx
        config = ps.Decoder.default_config()
        config.set_string('-keyphrase', self.wake_word)
        config.set_float('-kws_threshold', 1e-20)  # Adjust threshold as needed
        decoder = ps.Decoder(config)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        decoder.start_utt()

        while self.is_listening:
            buf = stream.read(1024)
            decoder.process_raw(buf, False, False)
            if decoder.hyp() is not None:
                if self.callback:
                    self.callback()
                decoder.end_utt()
                decoder.start_utt()

        stream.stop_stream()
        stream.close()
        p.terminate()
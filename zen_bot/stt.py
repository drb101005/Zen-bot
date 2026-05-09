from faster_whisper import WhisperModel

class STT:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(model_size, device="auto", compute_type="int8")

    def transcribe(self, audio_file):
        """
        Transcribe audio file to text.
        """
        segments, info = self.model.transcribe(audio_file, beam_size=5)
        text = ""
        for segment in segments:
            text += segment.text
        return text.strip()
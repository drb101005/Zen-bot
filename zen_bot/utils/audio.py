import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

def record_audio(duration=None, silence_threshold=0.01, silence_duration=2.0, sample_rate=16000):
    """
    Record audio until silence or duration.
    Returns the recorded audio data and sample rate.
    """
    audio_data = []
    silence_counter = 0
    chunk_duration = 0.1  # 100ms chunks
    chunk_samples = int(sample_rate * chunk_duration)

    def callback(indata, frames, time, status):
        nonlocal silence_counter
        audio_data.append(indata.copy())
        # Simple silence detection based on RMS
        rms = np.sqrt(np.mean(indata**2))
        if rms < silence_threshold:
            silence_counter += chunk_duration
        else:
            silence_counter = 0

    stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate)
    stream.start()

    if duration:
        sd.sleep(int(duration * 1000))
    else:
        while silence_counter < silence_duration:
            sd.sleep(int(chunk_duration * 1000))

    stream.stop()
    stream.close()

    # Concatenate audio data
    audio = np.concatenate(audio_data, axis=0)
    return audio.flatten(), sample_rate

def save_audio_to_wav(audio, sample_rate, filename=None):
    """
    Save audio data to a temporary WAV file.
    Returns the file path.
    """
    if filename is None:
        fd, filename = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
    wav.write(filename, sample_rate, (audio * 32767).astype(np.int16))
    return filename
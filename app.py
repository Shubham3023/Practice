import pyaudio
from vosk import Model, KaldiRecognizer
import sys
import json

# Set the sampling rate and the number of channels
sample_rate = 16000
num_channels = 1  # Mono

# Initialize Vosk recognizer
model_path = "vosk-model-en-us-0.22-lgraph"
model = Model(model_path)
recognizer = KaldiRecognizer(model, sample_rate)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open an audio stream
stream = audio.open(format=pyaudio.paInt16,
                    channels=num_channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=4096)

# Start the audio stream
print("Recording started. Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the stream
        data = stream.read(4096)

        # Feed the audio data to the recognizer
        if recognizer.AcceptWaveform(data):
            # Get the recognized speech
            result = recognizer.Result()
            text = json.loads(result)['text']
            print(text)

except KeyboardInterrupt:
    # Ctrl+C was pressed
    pass

# Stop the audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
audio.terminate()
print("Recording stopped.")
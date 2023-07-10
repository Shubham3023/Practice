import pyaudio
import wave
from vosk import Model, KaldiRecognizer

# Set the desired sample rate and duration
sample_rate = 16000  # Sample rate (Hz)
duration = 10  # Duration of recording (seconds)

# Set the input and output device indices (change as per your system)
input_device_index = 0  # Microphone input device index
output_device_index = 1  # Speaker output device index

# Initialize Vosk recognizer
model_path = "vosk-model-en-us-0.22-lgraph"
model = Model(model_path)
recognizer = KaldiRecognizer(model, sample_rate)

# Open the microphone and speaker streams
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    input_device_index=input_device_index,
                    output_device_index=output_device_index,
                    frames_per_buffer=4096)

# Open the audio file for recording
recording_file = wave.open('recording.wav', 'wb')
recording_file.setnchannels(1)
recording_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
recording_file.setframerate(sample_rate)

# Start the recording and playback
print("Recording started. Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the microphone and speaker
        data = stream.read(4096)

        # Write audio data to the recording file
        recording_file.writeframes(data)

        # Feed the audio data to the recognizer
        if recognizer.AcceptWaveform(data):
            # Get the recognized speech
            result = recognizer.Result()
            text = result["text"].strip()
            print("Recognized:", text)

except KeyboardInterrupt:
    # Ctrl+C was pressed
    pass

# Stop the stream and close the recording file
stream.stop_stream()
stream.close()
recording_file.close()

# Terminate PyAudio
audio.terminate()

print("Recording stopped.")
import sounddevice as sd
import numpy as np

def callback(indata, outdata, frames, time, status):
    outdata[:] = indata  # Passes microphone input to system speaker

# Set the sample rate and duration for recording
sample_rate = 44100  # Can adjust this value as needed
duration = 5  # Duration of recording in seconds

# Start the audio stream for recording
with sd.Stream(callback=callback, channels=2):
    print("Recording started...")
    # Record audio from the system speaker and microphone
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to finish

# Play the recorded audio from the system speaker
print("Recording finished. Playing audio...")
sd.play(recording, samplerate=sample_rate)
sd.wait()  # Wait for the playback to finish

print("Playback finished.")
import sounddevice as sd
import soundfile as sf

# Set up audio parameters
duration = 5  # Recording duration in seconds
fs = 44100  # Sample rate
channels = 2  # Number of audio channels

# Start recording from the headset speaker and microphone
print("Recording started...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, blocking=True)

# Save the recorded audio to a WAV file
sf.write("output.wav", recording, fs)

print("Recording finished.")
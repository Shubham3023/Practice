import pyaudio
import wave

# Set up audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Find and print available audio devices
for i in range(audio.get_device_count()):
    dev_info = audio.get_device_info_by_index(i)
    print("Device index:", i, " - ", dev_info["name"])

# Set the device indices for microphone and speaker

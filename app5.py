import sounddevice as sd
import numpy as np
import soundfile as sf

# Constants for audio recording
duration = 300  # Recording duration in seconds
sample_rate = 44100  # Sample rate
channels = 2  # Number of audio channels (stereo)
frames_per_buffer = 1024  # Number of frames per buffer

# Get available input and output devices
input_devices = sd.query_devices(kind='input')
output_devices = sd.query_devices(kind='output')

# Check if there are available input and output devices
if len(input_devices) == 0 or len(output_devices) == 0:
    print("No input or output devices found. Make sure your audio devices are connected.")
    exit(1)

# Select the first available input device
input_device_id = input_devices[0]['index']

# Select the first available output device
output_device_id = output_devices[0]['index']

# Initialize the recording buffers
recording = np.zeros((int(duration * sample_rate), channels), dtype=np.float32)

# Callback function to capture audio from input and output devices
def callback(indata, outdata, frames, time, status):
    # Capture audio from the input device (microphone)
    recording[i * frames:(i + 1) * frames, :] = indata

    # Pass through audio from the output device (speaker)
    outdata[:] = indata

# Start the audio stream for recording
with sd.Stream(device=(input_device_id, output_device_id),
               samplerate=sample_rate,
               channels=channels,
               frames_per_buffer=frames_per_buffer,
               callback=callback):
    print("Recording started. Press Ctrl+C to stop recording.")
    try:
        i = 0
        while i * frames_per_buffer < int(duration * sample_rate):
            sd.sleep(frames_per_buffer / sample_rate)
            i += 1
    except KeyboardInterrupt:
        pass

# Save the recording to a WAV file
output_file = "meeting_recording.wav"
sf.write(output_file, recording, sample_rate)

print("Meeting recording saved to:", output_file)
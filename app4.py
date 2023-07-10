import pyaudio
import wave

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10  # Recording duration (in seconds)
WAVE_OUTPUT_FILENAME = "meeting_recording.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Get available audio devices
device_info = audio.get_default_host_api_info()
input_device_id = None
output_device_id = None

# Search for headset microphone and speaker devices
for i in range(device_info['deviceCount']):
    device = audio.get_device_info_by_host_api_device_index(device_info['index'], i)
    if device['maxInputChannels'] > 0 and 'headset' in device['name'].lower():
        input_device_id = device['index']
    elif device['maxOutputChannels'] > 0 and 'headset' in device['name'].lower():
        output_device_id = device['index']

# Check if headset microphone and speaker devices are found
if input_device_id is None or output_device_id is None:
    print("Headset microphone or speaker not found. Please make sure your headset is connected.")
    exit(1)

# Open audio stream for recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=input_device_id)

# Open audio stream for playback
output_stream = audio.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           frames_per_buffer=CHUNK,
                           output_device_index=output_device_id)

print("Recording started. Press Ctrl+C to stop recording.")

frames = []

try:
    # Capture audio frames from the microphone and play them through the speaker
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        data1 = output_stream.read(CHUNK)
        frames.append(data)
        frames.append(data1)

except KeyboardInterrupt:
    print("Recording stopped.")

finally:
    # Stop recording and playback
    stream.stop_stream()
    stream.close()
    output_stream.stop_stream()
    output_stream.close()
    audio.terminate()

    # Save the recorded frames to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Meeting recording saved to:", WAVE_OUTPUT_FILENAME)
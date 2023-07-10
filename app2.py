import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
import json

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

# Create the audio streams for recording and playback
recording_frames = []
playback_frames = []

def audio_callback(indata, outdata, frames, time, status):
    # Store the input audio for recording
    recording_frames.append(indata.copy())

    # Pass the input audio to the output for playback
    if status.input_underflow:
        print("Input underflow:", status)
    if len(playback_frames) >= frames:
        outdata[:] = playback_frames[:frames]
        playback_frames[:] = playback_frames[frames:]
    else:
        outdata[:] = playback_frames

# Start the audio streams
input_stream = sd.InputStream(callback=audio_callback, channels=1,
                              device=input_device_index, samplerate=sample_rate)
output_stream = sd.OutputStream(callback=audio_callback, channels=1,
                                device=output_device_index, samplerate=sample_rate)

input_stream.start()
output_stream.start()

print("Recording started. Press Ctrl+C to stop.")

try:
    for _ in range(int(sample_rate / 4096 * duration)):
        # Read audio data from the microphone
        input_data, _ = input_stream.read(4096)

        # Write audio data to the recording frames
        recording_frames.append(input_data.copy())

        # Feed the audio data to the recognizer
        if recognizer.AcceptWaveform(input_data):
            # Get the recognized speech
            result = recognizer.Result()
            text = json.loads(result)['text']
            print("Recognized:", text)

        # Convert mono audio to stereo for playback
        output_data = sd.play(input_data, blocking=True, device=output_device_index)
        playback_frames.append(output_data.copy())

except KeyboardInterrupt:
    # Ctrl+C was pressed
    pass

print("Recording stopped.")

# Stop the audio streams
input_stream.stop()
output_stream.stop()

# Save the recorded audio to a file
recording_data = b''.join(recording_frames)
sf.write('recording.wav', recording_data, sample_rate)


'''

import sounddevice as sd
import soundfile as sf
import vosk

# Set the desired sample rate and duration
sample_rate = 16000  # Sample rate (Hz)
duration = 10  # Duration of recording (seconds)

# Set the input and output device indices (change as per your system)
input_device_index = 0  # Microphone input device index
output_device_index = 1  # Speaker output device index

# Initialize Vosk recognizer
model_path = "<path_to_model>"
recognizer = vosk.KaldiRecognizer(vosk.Model(model_path), sample_rate)

# Create the audio streams for recording and playback
recording_frames = []
playback_frames = []

def audio_callback(indata, outdata, frames, time, status):
    # Store the input audio for recording
    recording_frames.append(indata.copy())

    # Pass the input audio to the output for playback
    if status.input_underflow:
        print("Input underflow:", status)
    if len(playback_frames) >= frames:
        outdata[:] = playback_frames[:frames]
        playback_frames[:] = playback_frames[frames:]
    else:
        outdata[:] = playback_frames

# Start the audio streams
input_stream = sd.InputStream(callback=audio_callback, channels=1,
                              device=input_device_index, samplerate=sample_rate)
output_stream = sd.OutputStream(callback=audio_callback, channels=1,
                                device=output_device_index, samplerate=sample_rate)

input_stream.start()
output_stream.start()

print("Recording started. Press Ctrl+C to stop.")

try:
    for _ in range(int(sample_rate / 4096 * duration)):
        # Read audio data from the microphone
        input_data, _ = input_stream.read(4096)

        # Write audio data to the recording frames
        recording_frames.append(input_data.copy())

        # Feed the audio data to the recognizer
        if recognizer.AcceptWaveform(input_data):
            # Get the recognized speech
            result = recognizer.Result()
            text = result["text"].strip()
            print("Recognized:", text)

        # Convert mono audio to stereo for playback
        output_data = sd.play(input_data, blocking=True, device=output_device_index)
        playback_frames.append(output_data.copy())

except KeyboardInterrupt:
    # Ctrl+C was pressed
    pass

print("Recording stopped.")

# Stop the audio streams
input_stream.stop()
output_stream.stop()

# Save the recorded audio to a file
recording_data = b''.join(recording_frames)
sf.write('recording.wav', recording_data, sample_rate)'''
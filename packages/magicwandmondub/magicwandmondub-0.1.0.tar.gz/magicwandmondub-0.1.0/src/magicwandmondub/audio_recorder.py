import wave
import sounddevice as sd
import soundfile as sf
import queue
from . import config

# --- Configuration Constants ---
CHANNELS = config.DEFAULT_CHANNELS
AUDIO_EXTENSION = config.AUDIO_EXTENSION 
OUTPUT_DIR = config.OUTPUT_DIR
SAMPLE_RATE = config.SAMPLE_RATE
CHUNK_DURATION_S = config.CHUNK_DURATION_S  # Duration of each audio chunk in seconds
CHUNK_SIZE = config.CHUNK_SIZE  # Number of samples per chunk

class AudioRecorder:
    """Manages audio recording logic using sounddevice."""
    def __init__(self, samplerate=SAMPLE_RATE, channels=CHANNELS, chunk_size=CHUNK_SIZE):
        self.samplerate = samplerate
        self.channels = channels
        self._input_queue = queue.Queue() # Queue for non-blocking audio stream
        self._recording = False
        self._chunk_size = chunk_size
        self._stream = None
        self._selected_device_id = None # Device ID set by the UI
        self._audiofile_index = 0  # Index for saving audio files

    def get_input_devices(self):
        """Fetches available audio input devices using sounddevice.
        Returns a list of dictionaries: [{'id': int, 'name': str}]
        """
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append({'id': i, 'name': device['name']})
        return input_devices

    def set_device(self, device_id):
        """Sets the audio device ID to be used for recording."""
        self._selected_device_id = device_id

    def _audio_callback(self, indata, frames, time, status):
        """Callback function called by sounddevice for each audio block."""
        if status:
            # You might want to log these warnings or pass them back to the UI
            print(f"Audio stream status: {status}", flush=True)
        if self._recording: # Only put data if actively recording
            self._input_queue.put(bytes(indata))

    def start_recording(self, on_error_callback=None):
        """Starts the audio recording stream in a separate thread."""
        if self._recording:
            return False # Already recording

        if self._selected_device_id is None:
            if on_error_callback:
                on_error_callback("No audio device selected.")
            return False

        # Verify the selected device ID is valid
        try:
            device_info = sd.query_devices(self._selected_device_id, 'input')
            #Check supported channels
            if device_info['max_input_channels'] < self.channels:
                raise ValueError(f"Selected device '{device_info['name']}' does not support {self.channels} input channels.")

        except Exception as e:
            if on_error_callback:
                on_error_callback(f"Invalid device ID {self._selected_device_id}: {e}")
            print(f"Error querying device {self._selected_device_id}: {e}")
            return False

        self._recording = True
        print(f"Starting recording on device ID: {self._selected_device_id} at {self.samplerate} Hz, {self.channels} channel(s).")

        try:
            self._stream = sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                dtype='int16',
                device=self._selected_device_id,
                blocksize=self._chunk_size,
                callback=self._audio_callback
            )
            self._stream.start()
            return True
        except Exception as e:
            self._recording = False
            if on_error_callback:
                on_error_callback(f"Failed to start recording: {e}")
            print(f"Error starting recording: {e}")
            return False

    def get_chunk(self):
        """Retrieves the next audio chunk from the input queue."""
        try:
            if self._input_queue.qsize() > 0:
                audio_chunk = self._input_queue.get_nowait()
                return audio_chunk
        except queue.Empty:
            print("No audio data available in the queue.")    
        except Exception as e:
            print(f"Error consuming audio data: {e}")

        return None
    
    def save_audio_file(self, directory: str):
        """Saves all audio data from a queue into a WAV file."""
        print(f"Saving audio from queue to {directory}...")
        frames = []
        while not self._input_queue.empty():
            try:
                # Get audio data from the queue without blocking
                data = self._input_queue.get_nowait()
                frames.append(data)
            except queue.Empty:
                break
        
        if not frames:
            print(f"No audio data in queue to save for {directory}.")
            return

        # Filename with timestamp
        filename = f"{directory}/recording_{self._audiofile_index:03d}.{AUDIO_EXTENSION}"
        self._audiofile_index = (self._audiofile_index + 1) % 1000  # Increment index for next file

        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)  # 16-bit audio
        wave_file.setframerate(self.samplerate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        print(f"Successfully saved {filename}.")

    def stop_recording(self, save_callback=None, on_error_callback=None):
        """Stops the audio recording stream and triggers saving."""
        if not self._recording:
            return False # Not currently recording

        print("Stopping recording...")

        if self._stream and self._stream.active:
            self._stream.stop()
            self._stream.close()
            print("Recording stream stopped.")

        self._recording = False
        
    def get_audio_encoding(self, filename=None):
        """Returns the audio encoding format."""
        if filename:
            info = sf.info(filename, verbose=False)
            return info.subtype
        return sf.default_subtype(AUDIO_EXTENSION)

    @property
    def is_recording(self):
        """Returns True if recording is currently active."""
        return self._recording
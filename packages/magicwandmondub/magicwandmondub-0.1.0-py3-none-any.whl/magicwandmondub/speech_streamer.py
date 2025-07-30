import queue
import threading
from google.cloud import speech_v2
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import Unknown

class SpeechStreamer:
    """
    Manages a streaming connection to the Google Speech-to-Text v2 API,
    allowing for asynchronous audio sending and response handling.
    """

    def __init__(self, project_id: str, location: str, recognizer_id: str):
        self.project_id = project_id
        self.location = location
        self.recognizer_id = recognizer_id
        self._audio_queue = queue.Queue()
        self._is_closed = threading.Event()
        self._stream_thread = None

        # Initialize the Google Speech-to-Text client
        client_options = None
        if location != "global":
            api_endpoint = f"{location}-speech.googleapis.com"
            client_options = ClientOptions(api_endpoint=api_endpoint)

        self.client = speech_v2.SpeechClient(client_options=client_options)

    def _request_generator(self):
        """
        A generator that yields streaming recognition requests.
        It first sends the configuration, then pulls audio chunks from a queue.
        """
        try:
            recognizer_name = self.client.recognizer_path(
                self.project_id, self.location, self.recognizer_id
            )
            streaming_config = speech_v2.StreamingRecognitionConfig(
                config=speech_v2.RecognitionConfig(
                    # Explicitly define the audio encoding, sample rate, and channel count
                    explicit_decoding_config=speech_v2.ExplicitDecodingConfig(
                        encoding=speech_v2.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=16000,
                        audio_channel_count=1,
                    ),
                    language_codes=["mn-MN"],
                    # Using the more widely supported 'long' model for stability
                    model="long",
                ),
                streaming_features=speech_v2.StreamingRecognitionFeatures(
                    interim_results=True,
                ),
            )

            # The first request must include the recognizer and streaming config.
            print(">>> SpeechStreamer: Yielding initial config request.")
            yield speech_v2.StreamingRecognizeRequest(
                recognizer=recognizer_name, streaming_config=streaming_config
            )

            print(">>> SpeechStreamer: Initial config sent. Waiting for audio chunks.")
            

            while not self._is_closed.is_set():
                # Get the next audio chunk from the queue.
                # This will block until a chunk is available.
                chunk = self._audio_queue.get()
                
                # If the chunk is None, it's a signal to end the stream.
                if chunk is None:
                    print(">>> SpeechStreamer: Got None sentinel. Ending generator.")
                    return
                
                print(f">>> SpeechStreamer: Yielding audio chunk of size {len(chunk)} bytes.")
                yield speech_v2.StreamingRecognizeRequest(audio=chunk)
        except Exception as e:
            print(f"!!! SpeechStreamer: ERROR in request generator: {e}", flush=True)
            raise

    def _run_stream(self):
        """Target function for the background thread to process responses."""
        try:
            requests = self._request_generator()
            responses = self.client.streaming_recognize(requests=requests)
            
            print(">>> SpeechStreamer: Listening for responses...")
            for response in responses:
                for result in response.results:
                    if not result.alternatives:
                        continue
                    
                    is_final = " (final)" if result.is_final else ""
                    print(f"Transcript: {result.alternatives[0].transcript}{is_final}")
            
            print(">>> SpeechStreamer: Response stream finished.")
        except Unknown as e:
            print(f"!!! SpeechStreamer: ERROR - a gRPC 'Unknown' error occurred: {e}", flush=True)
            print("!!! This may be due to a network issue or an audio source problem.", flush=True)
        except Exception as e:
            print(f"!!! SpeechStreamer: ERROR in stream thread: {e}", flush=True)
        finally:
            self._is_closed.set()

    def process_streaming_responses(self, responses):
        """
        Filters duplicate text from a list of streaming API responses
        and forms a complete sentence.

        Args:
            responses (list of str): A list of text responses from the speech-to-text API.

        Returns:
            str: A complete and filtered sentence.
        """
        final_sentence = ""
        for response in responses:
            # Check if the new response starts with the already formed sentence.
            # The 'strip()' is used to handle potential leading/trailing whitespace.
            if response.strip().startswith(final_sentence.strip()):
                # Find the new, unique part of the response.
                new_part = response.strip()[len(final_sentence.strip()):]
                # Append the new part to the final sentence.
                final_sentence += new_part
            else:
                # This handles cases where a new sentence starts without overlap.
                final_sentence = response.strip()

        return final_sentence.strip()

    def start(self):
        """Starts the streaming connection in a background thread."""
        if self._stream_thread is not None:
            print("Stream is already running.")
            return

        print(">>> Starting the stream...")
        self._stream_thread = threading.Thread(target=self._run_stream)
        self._stream_thread.start()

    def send_audio(self, audio_chunk: bytes):
        """
        Sends an audio chunk to the stream. This method can be called from
        any thread.
        """
        if self._is_closed.is_set() or self._stream_thread is None:
            print("Cannot send audio, stream is not running.", flush=True)
            return
        
        # Add the audio chunk to the queue.
        self._audio_queue.put(audio_chunk)

    def close(self):
        """
        Closes the stream gracefully. It signals the generator to stop
        and waits for the background thread to finish.
        """
        if self._stream_thread is None:
            return
        print(">>> SpeechStreamer: Closing...")
        self._is_closed.set()
        self._audio_queue.put(None)
        self._stream_thread.join()
        self._stream_thread = None
        print(">>> SpeechStreamer: Closed.")

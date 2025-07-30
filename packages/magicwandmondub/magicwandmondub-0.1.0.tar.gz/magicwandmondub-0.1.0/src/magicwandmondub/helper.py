import numpy as np

def is_speech(chunk: bytes, threshold: int) -> bool:
    """
    Determines if an audio chunk contains speech by calculating its RMS energy.
    """
    # Convert the byte string chunk back into a numpy array of 16-bit integers
    audio_samples = np.frombuffer(chunk, dtype=np.int16)
    
    # Calculate the Root Mean Square of the audio samples
    rms = np.sqrt(np.mean(audio_samples.astype(np.float32)**2))
    
    return rms > threshold
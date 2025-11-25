import os

class SpeechService:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from faster_whisper import WhisperModel
            print(f"Loading Whisper model ({self.model_size})...")
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            print("Whisper model loaded.")
        except ImportError:
            print("WARNING: faster-whisper not found. Speech-to-text will be disabled.")
        except Exception as e:
            print(f"ERROR: Failed to load Whisper model: {e}")

    def transcribe(self, audio_path):
        """
        Transcribes the given audio file.
        Returns the transcribed text or None if failed.
        """
        if not self.model:
            print("Error: Whisper model is not loaded.")
            return None

        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found at {audio_path}")
            return None

        try:
            segments, info = self.model.transcribe(audio_path, beam_size=5)
            
            print(f"Detected language '{info.language}' with probability {info.language_probability}")
            
            # Collect all segments
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

if __name__ == "__main__":
    # Test
    # Create a dummy file or use an existing one if available for testing
    service = SpeechService()
    print("SpeechService initialized.")

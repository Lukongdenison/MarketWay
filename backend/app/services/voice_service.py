import os
import speech_recognition as sr
from gtts import gTTS
import uuid
from app.core.config import settings

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Ensure temp dir exists for audio files
        self.temp_dir = os.path.join(settings.BASE_DIR, "temp_audio")
        os.makedirs(self.temp_dir, exist_ok=True)

    def speech_to_text(self, audio_file_path: str) -> str:
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error processing audio: {e}"

    def text_to_speech(self, text: str) -> str:
        try:
            # Generate unique filename
            filename = f"response_{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            tts = gTTS(text=text, lang='en')
            tts.save(filepath)
            
            return filepath
        except Exception as e:
            print(f"Error generating speech: {e}")
            return ""

voice_service = VoiceService()

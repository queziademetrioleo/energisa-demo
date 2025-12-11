"""ElevenLabs TTS service."""
from elevenlabs import generate, stream, Voice, VoiceSettings
from ..config import settings


class ElevenLabsService:
    """ElevenLabs Text-to-Speech service."""

    def __init__(self):
        """Initialize ElevenLabs client."""
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id

    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech."""
        try:
            print(f'🔊 Generating speech for: {text[:50]}...')

            # Generate audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=self.voice_id,
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.75,
                        style=0.5,
                        use_speaker_boost=True,
                    )
                ),
                model='eleven_turbo_v2_5',  # Fastest model for real-time
                api_key=self.api_key,
            )

            # Convert generator to bytes
            audio_bytes = b''.join(audio)

            print(f'✅ Generated audio: {len(audio_bytes)} bytes')
            return audio_bytes

        except Exception as e:
            print(f'❌ ElevenLabs error: {e}')
            raise

    async def text_to_speech_stream(self, text: str):
        """Convert text to speech with streaming."""
        try:
            audio_stream = generate(
                text=text,
                voice=Voice(
                    voice_id=self.voice_id,
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.75,
                        style=0.5,
                        use_speaker_boost=True,
                    )
                ),
                model='eleven_turbo_v2_5',
                stream=True,
                api_key=self.api_key,
            )

            # Stream audio
            for chunk in audio_stream:
                yield chunk

        except Exception as e:
            print(f'❌ ElevenLabs streaming error: {e}')
            raise

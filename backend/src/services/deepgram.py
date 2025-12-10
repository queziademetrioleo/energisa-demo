"""Deepgram STT service."""
import asyncio
from typing import Optional, Callable
from deepgram import Deepgram
from ..config import settings


class DeepgramService:
    """Deepgram Speech-to-Text service."""

    def __init__(self):
        """Initialize Deepgram client."""
        self.client = Deepgram(settings.deepgram_api_key)
        self.connection: Optional[any] = None
        self.on_transcript: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

    async def start_streaming(self):
        """Start streaming transcription."""
        try:
            options = {
                'model': 'nova-2',
                'language': 'pt-BR',
                'smart_format': True,
                'interim_results': True,
                'punctuate': True,
                'utterance_end_ms': 1000,
                'vad_events': True,
            }

            self.connection = await self.client.transcription.live(options)

            # Set up event handlers
            self.connection.on('open', self._on_open)
            self.connection.on('transcript_received', self._on_transcript_received)
            self.connection.on('error', self._on_error)
            self.connection.on('close', self._on_close)

            print('✅ Deepgram connection opened')

        except Exception as e:
            print(f'❌ Failed to start Deepgram streaming: {e}')
            raise

    def _on_open(self):
        """Handle connection open."""
        print('🔊 Deepgram ready to receive audio')

    def _on_transcript_received(self, data):
        """Handle transcript received."""
        try:
            transcript = data['channel']['alternatives'][0]['transcript']

            if transcript and transcript.strip():
                result = {
                    'transcript': transcript,
                    'is_final': data.get('is_final', False),
                    'confidence': data['channel']['alternatives'][0].get('confidence'),
                }

                if self.on_transcript:
                    asyncio.create_task(self.on_transcript(result))

        except Exception as e:
            print(f'❌ Error processing transcript: {e}')

    def _on_error(self, error):
        """Handle error."""
        print(f'❌ Deepgram error: {error}')
        if self.on_error:
            asyncio.create_task(self.on_error(error))

    def _on_close(self):
        """Handle connection close."""
        print('🔌 Deepgram connection closed')

    async def send_audio(self, audio_data: bytes):
        """Send audio data to Deepgram."""
        if self.connection:
            await self.connection.send(audio_data)

    async def close(self):
        """Close connection."""
        if self.connection:
            await self.connection.finish()
            self.connection = None

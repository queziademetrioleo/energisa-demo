"""Voice Agent orchestrator."""
import asyncio
import time
from typing import Optional
from ..models import SessionState, ConversationMessage, STTResult
from ..services.deepgram import DeepgramService
from ..services.gemini import GeminiService
from ..services.elevenlabs import ElevenLabsService
from .gisa_prompt import GISA_INITIAL_MESSAGE, GISA_SYSTEM_PROMPT


class VoiceAgent:
    """Voice agent that orchestrates STT, LLM, and TTS."""

    def __init__(self, session_id: str):
        """Initialize voice agent."""
        self.session_id = session_id
        self.stt_service = DeepgramService()
        self.llm_service = GeminiService()
        self.tts_service = ElevenLabsService()

        self.session_state = SessionState(
            session_id=session_id,
            conversation_history=[
                ConversationMessage(
                    role='system',
                    content=GISA_SYSTEM_PROMPT,
                    timestamp=time.time(),
                )
            ],
            current_phase='FASE_1',
            uc_validated=False,
            start_time=time.time(),
        )

        self.interim_transcript = ''
        self.is_processing = False
        self.on_audio_callback: Optional[callable] = None
        self.on_response_callback: Optional[callable] = None

    async def initialize(self):
        """Initialize the voice agent."""
        try:
            print('🚀 Initializing voice agent...')

            # Start STT streaming
            await self.stt_service.start_streaming()

            # Set up STT callbacks
            self.stt_service.on_transcript = self._handle_transcript
            self.stt_service.on_error = self._handle_error

            # Generate and send initial greeting
            await self._send_initial_greeting()

            print('✅ Voice agent initialized')

        except Exception as e:
            print(f'❌ Failed to initialize voice agent: {e}')
            raise

    async def _send_initial_greeting(self):
        """Send initial greeting."""
        try:
            # Add to conversation history
            self.session_state.conversation_history.append(
                ConversationMessage(
                    role='assistant',
                    content=GISA_INITIAL_MESSAGE,
                    timestamp=time.time(),
                )
            )

            # Generate audio
            audio_bytes = await self.tts_service.text_to_speech(GISA_INITIAL_MESSAGE)

            # Emit audio
            if self.on_audio_callback:
                await self.on_audio_callback(audio_bytes)

        except Exception as e:
            print(f'❌ Failed to send initial greeting: {e}')
            raise

    async def _handle_transcript(self, result: dict):
        """Handle transcript from STT."""
        if result['is_final']:
            print(f"📝 Final transcript: {result['transcript']}")
            self.interim_transcript = ''

            if not self.is_processing:
                await self._process_user_input(result['transcript'])
        else:
            self.interim_transcript = result['transcript']
            print(f"💭 Interim: {self.interim_transcript}")

    async def _handle_error(self, error):
        """Handle STT error."""
        print(f'❌ STT Error: {error}')

    async def _process_user_input(self, transcript: str):
        """Process user input."""
        if self.is_processing or not transcript.strip():
            return

        self.is_processing = True

        try:
            print(f'🎯 Processing user input: {transcript}')

            # Add user message to history
            self.session_state.conversation_history.append(
                ConversationMessage(
                    role='user',
                    content=transcript,
                    timestamp=time.time(),
                )
            )

            # Get LLM response
            llm_response = await self.llm_service.generate_response(
                self.session_state.conversation_history
            )

            print(f'🤖 LLM Response: {llm_response.text}')

            # Update session state based on metadata
            if llm_response.metadata:
                if 'phase' in llm_response.metadata:
                    self.session_state.current_phase = llm_response.metadata['phase']

                # Check if UC was validated
                if (
                    'validei' in llm_response.text.lower()
                    or 'perfeito' in llm_response.text.lower()
                ):
                    self.session_state.uc_validated = True

            # Add assistant response to history
            self.session_state.conversation_history.append(
                ConversationMessage(
                    role='assistant',
                    content=llm_response.text,
                    timestamp=time.time(),
                )
            )

            # Generate speech
            audio_bytes = await self.tts_service.text_to_speech(llm_response.text)

            # Emit audio
            if self.on_audio_callback:
                await self.on_audio_callback(audio_bytes)

            # Emit response for UI
            if self.on_response_callback:
                await self.on_response_callback({
                    'text': llm_response.text,
                    'metadata': llm_response.metadata,
                })

        except Exception as e:
            print(f'❌ Error processing user input: {e}')
        finally:
            self.is_processing = False

    async def process_audio(self, audio_data: bytes):
        """Process incoming audio."""
        await self.stt_service.send_audio(audio_data)

    def get_session_state(self) -> SessionState:
        """Get current session state."""
        return self.session_state

    async def shutdown(self):
        """Shutdown the voice agent."""
        print('🛑 Shutting down voice agent...')
        await self.stt_service.close()

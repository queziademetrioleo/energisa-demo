"""Google Gemini LLM service."""
import google.generativeai as genai
from typing import List, Dict
from ..config import settings
from ..models import ConversationMessage, LLMResponse
from ..agent.gisa_prompt import GISA_SYSTEM_PROMPT


class GeminiService:
    """Google Gemini LLM service."""

    def __init__(self):
        """Initialize Gemini client."""
        genai.configure(api_key=settings.google_api_key)

        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 500,  # Keep responses concise for voice
            },
        )

    async def generate_response(
        self, conversation_history: List[ConversationMessage]
    ) -> LLMResponse:
        """Generate response from conversation history."""
        try:
            # Build conversation context
            messages = []

            # Add system prompt first
            messages.append({'role': 'user', 'parts': [GISA_SYSTEM_PROMPT]})
            messages.append({'role': 'model', 'parts': ['Entendido. Vou seguir essas diretrizes.']})

            # Add conversation history
            for msg in conversation_history:
                if msg.role == 'system':
                    continue  # Skip system messages

                role = 'model' if msg.role == 'assistant' else 'user'
                messages.append({'role': role, 'parts': [msg.content]})

            # Start chat with history (excluding last message)
            chat = self.model.start_chat(history=messages[:-1])

            # Send last message
            last_message = messages[-1]['parts'][0]
            response = await asyncio.to_thread(chat.send_message, last_message)

            text = response.text
            print(f'🤖 Gemini response: {text[:100]}...')

            return LLMResponse(
                text=text,
                metadata=self._extract_metadata(text)
            )

        except Exception as e:
            print(f'❌ Gemini error: {e}')
            raise

    def _extract_metadata(self, text: str) -> Dict:
        """Extract metadata from response."""
        metadata = {}

        # Extract protocol numbers
        import re
        protocol_match = re.search(r'DEMO-[\w-]+', text)
        if protocol_match:
            metadata['protocol'] = protocol_match.group(0)

        # Detect phase
        if 'Com quem eu falo' in text or 'FASE_1' in text:
            metadata['phase'] = 'FASE_1'
        elif 'Unidade Consumidora' in text or 'UC' in text:
            metadata['phase'] = 'FASE_2'
        else:
            metadata['phase'] = 'FASE_3'

        return metadata


# Import asyncio for async operations
import asyncio

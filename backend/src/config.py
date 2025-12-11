"""Configuration management."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class Settings(BaseSettings):
    """Application settings."""

    # LiveKit
    livekit_url: str = os.getenv('LIVEKIT_URL', 'ws://localhost:7880')
    livekit_api_key: str = os.getenv('LIVEKIT_API_KEY', '')
    livekit_api_secret: str = os.getenv('LIVEKIT_API_SECRET', '')

    # Deepgram (STT)
    deepgram_api_key: str = os.getenv('DEEPGRAM_API_KEY', '')

    # Google Gemini (LLM)
    google_api_key: str = os.getenv('GOOGLE_API_KEY', '')

    # ElevenLabs (TTS)
    elevenlabs_api_key: str = os.getenv('ELEVENLABS_API_KEY', '')
    elevenlabs_voice_id: str = os.getenv('ELEVENLABS_VOICE_ID', '')

    # Server
    port: int = int(os.getenv('PORT', '3000'))
    host: str = os.getenv('HOST', '0.0.0.0')
    env: str = os.getenv('NODE_ENV', 'development')

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()


def validate_config() -> None:
    """Validate required configuration."""
    required = {
        'LIVEKIT_API_KEY': settings.livekit_api_key,
        'LIVEKIT_API_SECRET': settings.livekit_api_secret,
        'DEEPGRAM_API_KEY': settings.deepgram_api_key,
        'GOOGLE_API_KEY': settings.google_api_key,
        'ELEVENLABS_API_KEY': settings.elevenlabs_api_key,
        'ELEVENLABS_VOICE_ID': settings.elevenlabs_voice_id,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        print('❌ Missing required environment variables:')
        for key in missing:
            print(f'   - {key}')
        print('\n📝 Please copy .env.example to .env and fill in the values')
        raise SystemExit(1)

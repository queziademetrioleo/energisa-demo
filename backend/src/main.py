"""FastAPI main application."""
import asyncio
import time
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
from .config import settings, validate_config
from .models import (
    TokenRequest,
    TokenResponse,
    SessionStartRequest,
    SessionResponse,
    HealthResponse,
)
from .agent.voice_agent import VoiceAgent

# Validate configuration on startup
validate_config()

app = FastAPI(
    title='GISA Voice Agent API',
    description='Backend API for GISA voice agent',
    version='1.0.0',
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Configure properly in production
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Store active sessions
active_sessions: Dict[str, VoiceAgent] = {}


@app.on_event('startup')
async def startup_event():
    """Startup event."""
    print('')
    print('🎙️  ========================================')
    print('🎙️   GISA - Voice Agent Server (Python)')
    print('🎙️  ========================================')
    print('')
    print(f'✅ Server starting on {settings.host}:{settings.port}')
    print(f'🔗 LiveKit URL: {settings.livekit_url}')
    print('')
    print('📡 Services:')
    print('   - Deepgram (STT): ✓')
    print('   - Gemini 2.0 Flash (LLM): ✓')
    print('   - ElevenLabs (TTS): ✓')
    print('')
    print('🚀 Ready to accept connections!')
    print('')


@app.on_event('shutdown')
async def shutdown_event():
    """Shutdown event."""
    print('\n🛑 Shutting down server...')

    # Shutdown all active sessions
    for session_id, agent in active_sessions.items():
        print(f'   Ending session: {session_id}')
        await agent.shutdown()

    active_sessions.clear()


@app.get('/health', response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status='healthy',
        timestamp=datetime.now().isoformat(),
        active_sessions=len(active_sessions),
    )


@app.post('/api/token', response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    """Generate LiveKit token for client."""
    try:
        token = api.AccessToken(
            settings.livekit_api_key,
            settings.livekit_api_secret,
        )

        token.with_identity(request.participant_name)
        token.with_name(request.participant_name)
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=request.room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            )
        )

        jwt_token = token.to_jwt()

        print(
            f'🎫 Generated token for {request.participant_name} in room {request.room_name}'
        )

        return TokenResponse(
            token=jwt_token,
            url=settings.livekit_url,
        )

    except Exception as e:
        print(f'❌ Error generating token: {e}')
        raise HTTPException(status_code=500, detail='Failed to generate token')


@app.post('/api/session/start', response_model=SessionResponse)
async def start_session(request: SessionStartRequest):
    """Start a new voice agent session."""
    try:
        # Create voice agent
        agent = VoiceAgent(request.session_id)

        # TODO: Connect to LiveKit room and handle audio streams
        # This requires additional LiveKit integration for Python

        # Initialize agent
        await agent.initialize()

        # Store session
        active_sessions[request.session_id] = agent

        print(f'✅ Session started: {request.session_id}')

        return SessionResponse(
            session_id=request.session_id,
            status='active',
            phase=agent.get_session_state().current_phase,
        )

    except Exception as e:
        print(f'❌ Error starting session: {e}')
        raise HTTPException(status_code=500, detail='Failed to start session')


@app.get('/api/session/{session_id}', response_model=SessionResponse)
async def get_session(session_id: str):
    """Get session status."""
    agent = active_sessions.get(session_id)

    if not agent:
        raise HTTPException(status_code=404, detail='Session not found')

    state = agent.get_session_state()

    return SessionResponse(
        session_id=session_id,
        status='active',
        phase=state.current_phase,
        uc_validated=state.uc_validated,
        message_count=len(state.conversation_history),
        uptime=time.time() - state.start_time,
    )


@app.post('/api/session/{session_id}/end', response_model=SessionResponse)
async def end_session(session_id: str):
    """End a session."""
    agent = active_sessions.get(session_id)

    if not agent:
        raise HTTPException(status_code=404, detail='Session not found')

    await agent.shutdown()
    active_sessions.pop(session_id)

    print(f'🛑 Session ended: {session_id}')

    return SessionResponse(
        session_id=session_id,
        status='ended',
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'src.main:app',
        host=settings.host,
        port=settings.port,
        reload=settings.env == 'development',
    )

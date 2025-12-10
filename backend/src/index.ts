import express from 'express';
import { AccessToken } from 'livekit-server-sdk';
import config, { validateConfig } from './config';
import { VoiceAgent } from './agent/voiceAgent';
import { Room, RoomEvent, RemoteParticipant } from '@livekit/rtc-node';

// Validate configuration
validateConfig();

const app = express();
app.use(express.json());

// Store active sessions
const activeSessions = new Map<string, VoiceAgent>();

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    activeSessions: activeSessions.size,
  });
});

// Generate LiveKit token for client
app.post('/api/token', async (req, res) => {
  try {
    const { roomName, participantName } = req.body;

    if (!roomName || !participantName) {
      return res.status(400).json({
        error: 'roomName and participantName are required',
      });
    }

    const token = new AccessToken(
      config.livekit.apiKey,
      config.livekit.apiSecret,
      {
        identity: participantName,
        name: participantName,
      }
    );

    token.addGrant({
      roomJoin: true,
      room: roomName,
      canPublish: true,
      canSubscribe: true,
      canPublishData: true,
    });

    const jwt = await token.toJwt();

    console.log(`🎫 Generated token for ${participantName} in room ${roomName}`);

    res.json({
      token: jwt,
      url: config.livekit.url,
    });
  } catch (error) {
    console.error('❌ Error generating token:', error);
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

// Start voice agent session
app.post('/api/session/start', async (req, res) => {
  try {
    const { sessionId, roomName } = req.body;

    if (!sessionId || !roomName) {
      return res.status(400).json({
        error: 'sessionId and roomName are required',
      });
    }

    // Create voice agent
    const agent = new VoiceAgent(sessionId);

    // Connect to LiveKit room
    const room = new Room();

    // Handle room events
    room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
      console.log(`🎵 Track subscribed: ${track.kind} from ${participant.identity}`);

      if (track.kind === 'audio') {
        // Process incoming audio
        track.on('frame', (frame: any) => {
          // Send audio to STT
          agent.processAudio(Buffer.from(frame.data));
        });
      }
    });

    room.on(RoomEvent.ParticipantConnected, (participant: RemoteParticipant) => {
      console.log(`👤 Participant connected: ${participant.identity}`);
    });

    // Handle agent audio output
    agent.on('audio', async (audioBuffer: Buffer) => {
      try {
        // Publish audio to room
        // Note: You'll need to create an audio track from the buffer
        console.log('🔊 Publishing audio to room:', audioBuffer.length, 'bytes');

        // TODO: Implement audio track publishing
        // This requires converting the PCM buffer to an audio track
      } catch (error) {
        console.error('❌ Error publishing audio:', error);
      }
    });

    // Initialize agent
    await agent.initialize();

    // Connect to room
    const token = new AccessToken(
      config.livekit.apiKey,
      config.livekit.apiSecret,
      {
        identity: `agent-${sessionId}`,
        name: 'GISA',
      }
    );

    token.addGrant({
      roomJoin: true,
      room: roomName,
      canPublish: true,
      canSubscribe: true,
    });

    const jwt = await token.toJwt();

    await room.connect(config.livekit.url, jwt);

    // Store session
    activeSessions.set(sessionId, agent);

    console.log(`✅ Session started: ${sessionId}`);

    res.json({
      sessionId,
      status: 'active',
      phase: agent.getSessionState().currentPhase,
    });
  } catch (error) {
    console.error('❌ Error starting session:', error);
    res.status(500).json({ error: 'Failed to start session' });
  }
});

// Get session status
app.get('/api/session/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  const agent = activeSessions.get(sessionId);

  if (!agent) {
    return res.status(404).json({ error: 'Session not found' });
  }

  const state = agent.getSessionState();

  res.json({
    sessionId,
    status: 'active',
    phase: state.currentPhase,
    ucValidated: state.ucValidated,
    messageCount: state.conversationHistory.length,
    uptime: Date.now() - state.startTime,
  });
});

// End session
app.post('/api/session/:sessionId/end', async (req, res) => {
  const { sessionId } = req.params;
  const agent = activeSessions.get(sessionId);

  if (!agent) {
    return res.status(404).json({ error: 'Session not found' });
  }

  await agent.shutdown();
  activeSessions.delete(sessionId);

  console.log(`🛑 Session ended: ${sessionId}`);

  res.json({ sessionId, status: 'ended' });
});

// Start server
const PORT = config.server.port;

app.listen(PORT, () => {
  console.log('');
  console.log('🎙️  ========================================');
  console.log('🎙️   GISA - Voice Agent Server');
  console.log('🎙️  ========================================');
  console.log('');
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`🌐 LiveKit URL: ${config.livekit.url}`);
  console.log('');
  console.log('📡 Services:');
  console.log('   - Deepgram (STT): ✓');
  console.log('   - Gemini 2.5 Flash (LLM): ✓');
  console.log('   - ElevenLabs (TTS): ✓');
  console.log('');
  console.log('🚀 Ready to accept connections!');
  console.log('');
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down server...');

  // Shutdown all active sessions
  for (const [sessionId, agent] of activeSessions.entries()) {
    console.log(`   Ending session: ${sessionId}`);
    await agent.shutdown();
  }

  activeSessions.clear();
  process.exit(0);
});

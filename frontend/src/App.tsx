import { useState, useEffect, useRef } from 'react';
import { Room, RoomEvent, Track } from 'livekit-client';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

type ConnectionState = 'disconnected' | 'connecting' | 'connected';
type AgentState = 'idle' | 'listening' | 'thinking' | 'speaking';

function App() {
  const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected');
  const [agentState, setAgentState] = useState<AgentState>('idle');
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [sessionId] = useState(() => `session-${Date.now()}`);
  const [roomName] = useState(() => `gisa-room-${Date.now()}`);

  const roomRef = useRef<Room | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (roomRef.current) {
        roomRef.current.disconnect();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  const connectToRoom = async () => {
    try {
      setConnectionState('connecting');
      setError(null);

      // Get token from backend
      const tokenResponse = await fetch('/api/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          roomName,
          participantName: `user-${Date.now()}`,
        }),
      });

      if (!tokenResponse.ok) {
        throw new Error('Failed to get token');
      }

      const { token, url } = await tokenResponse.json();

      // Create room
      const room = new Room({
        adaptiveStream: true,
        dynacast: true,
        videoCaptureDefaults: {
          resolution: { width: 1280, height: 720 },
        },
      });

      roomRef.current = room;

      // Set up event listeners
      room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
        console.log('Track subscribed:', track.kind, 'from', participant.identity);

        if (track.kind === Track.Kind.Audio) {
          // Agent is speaking
          setAgentState('speaking');

          const audioElement = track.attach();
          document.body.appendChild(audioElement);
          audioElement.play();

          track.on('ended', () => {
            audioElement.remove();
            setAgentState('listening');
          });
        }
      });

      room.on(RoomEvent.Connected, () => {
        console.log('Connected to room');
        setConnectionState('connected');
        setAgentState('listening');
      });

      room.on(RoomEvent.Disconnected, () => {
        console.log('Disconnected from room');
        setConnectionState('disconnected');
        setAgentState('idle');
      });

      // Connect to room
      await room.connect(url, token);

      // Enable microphone
      await room.localParticipant.setMicrophoneEnabled(true);

      // Start session on backend
      await fetch('/api/session/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          roomName,
        }),
      });

      console.log('Session started');

    } catch (err) {
      console.error('Connection error:', err);
      setError(err instanceof Error ? err.message : 'Failed to connect');
      setConnectionState('disconnected');
    }
  };

  const disconnect = async () => {
    try {
      if (roomRef.current) {
        roomRef.current.disconnect();
        roomRef.current = null;
      }

      // End session on backend
      await fetch(`/api/session/${sessionId}/end`, {
        method: 'POST',
      });

      setConnectionState('disconnected');
      setAgentState('idle');
    } catch (err) {
      console.error('Disconnect error:', err);
    }
  };

  const getStatusText = (): string => {
    if (connectionState === 'connecting') return 'Conectando...';
    if (connectionState === 'disconnected') return 'Desconectado';

    switch (agentState) {
      case 'listening': return 'Ouvindo...';
      case 'thinking': return 'Processando...';
      case 'speaking': return 'Falando...';
      default: return 'Conectado';
    }
  };

  const getStatusDotClass = (): string => {
    if (connectionState !== 'connected') return '';

    switch (agentState) {
      case 'listening': return 'listening';
      case 'speaking': return 'speaking';
      default: return 'connected';
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>🎙️ GISA</h1>
        <p>Assistente Inteligente da Energisa</p>
      </div>

      <div className="voice-interface">
        <div className="status">
          <div className={`status-dot ${getStatusDotClass()}`}></div>
          <span>{getStatusText()}</span>
        </div>

        <div
          className={`microphone ${connectionState === 'connected' ? 'active' : ''}`}
          onClick={connectionState === 'disconnected' ? connectToRoom : undefined}
          style={{ cursor: connectionState === 'disconnected' ? 'pointer' : 'default' }}
        >
          <svg viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
          </svg>
        </div>

        <div className="controls">
          {connectionState === 'disconnected' ? (
            <button
              className="btn btn-primary"
              onClick={connectToRoom}
            >
              Iniciar Conversa
            </button>
          ) : (
            <button
              className="btn btn-secondary"
              onClick={disconnect}
            >
              Encerrar
            </button>
          )}
        </div>

        {error && (
          <div className="error">
            <strong>Erro:</strong> {error}
          </div>
        )}

        {messages.length > 0 && (
          <div className="transcript">
            <h3>Transcrição</h3>
            <div className="messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  <div className="message-label">
                    {msg.role === 'user' ? 'Você' : 'GISA'}
                  </div>
                  <div>{msg.content}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

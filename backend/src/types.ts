export interface ConversationMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
}

export interface SessionState {
  sessionId: string;
  conversationHistory: ConversationMessage[];
  currentPhase: 'FASE_1' | 'FASE_2' | 'FASE_3';
  ucValidated: boolean;
  ucNumber?: string;
  startTime: number;
}

export interface AudioChunk {
  data: Buffer;
  sampleRate: number;
  channels: number;
}

export interface STTResult {
  transcript: string;
  isFinal: boolean;
  confidence?: number;
}

export interface TTSResult {
  audio: Buffer;
  contentType: string;
}

export interface LLMResponse {
  text: string;
  metadata?: {
    phase?: string;
    action?: string;
    scenario?: string;
  };
}

import { EventEmitter } from 'events';
import { DeepgramService } from '../services/deepgram';
import { GeminiService } from '../services/gemini';
import { ElevenLabsService } from '../services/elevenlabs';
import { SessionState, ConversationMessage, STTResult } from '../types';
import { GISA_INITIAL_MESSAGE, GISA_SYSTEM_PROMPT } from './gisaPrompt';

export class VoiceAgent extends EventEmitter {
  private sttService: DeepgramService;
  private llmService: GeminiService;
  private ttsService: ElevenLabsService;
  private sessionState: SessionState;
  private interimTranscript: string = '';
  private isProcessing: boolean = false;

  constructor(sessionId: string) {
    super();

    this.sttService = new DeepgramService();
    this.llmService = new GeminiService();
    this.ttsService = new ElevenLabsService();

    this.sessionState = {
      sessionId,
      conversationHistory: [
        {
          role: 'system',
          content: GISA_SYSTEM_PROMPT,
          timestamp: Date.now(),
        },
      ],
      currentPhase: 'FASE_1',
      ucValidated: false,
      startTime: Date.now(),
    };

    this.setupSTTListeners();
  }

  private setupSTTListeners(): void {
    this.sttService.on('transcript', async (result: STTResult) => {
      if (result.isFinal) {
        console.log('📝 Final transcript:', result.transcript);
        this.interimTranscript = '';

        if (!this.isProcessing) {
          await this.processUserInput(result.transcript);
        }
      } else {
        this.interimTranscript = result.transcript;
        console.log('💭 Interim:', this.interimTranscript);
      }
    });

    this.sttService.on('error', (error) => {
      console.error('❌ STT Error:', error);
      this.emit('error', error);
    });
  }

  async initialize(): Promise<void> {
    try {
      console.log('🚀 Initializing voice agent...');

      // Start STT streaming
      await this.sttService.startStreaming();

      // Generate and send initial greeting
      await this.sendInitialGreeting();

      console.log('✅ Voice agent initialized');
    } catch (error) {
      console.error('❌ Failed to initialize voice agent:', error);
      throw error;
    }
  }

  private async sendInitialGreeting(): Promise<void> {
    try {
      // Add to conversation history
      this.sessionState.conversationHistory.push({
        role: 'assistant',
        content: GISA_INITIAL_MESSAGE,
        timestamp: Date.now(),
      });

      // Generate audio
      const audioBuffer = await this.ttsService.textToSpeech(
        GISA_INITIAL_MESSAGE
      );

      // Emit audio to be sent via LiveKit
      this.emit('audio', audioBuffer);
    } catch (error) {
      console.error('❌ Failed to send initial greeting:', error);
      throw error;
    }
  }

  private async processUserInput(transcript: string): Promise<void> {
    if (this.isProcessing || !transcript.trim()) {
      return;
    }

    this.isProcessing = true;

    try {
      console.log('🎯 Processing user input:', transcript);

      // Add user message to history
      this.sessionState.conversationHistory.push({
        role: 'user',
        content: transcript,
        timestamp: Date.now(),
      });

      // Get LLM response
      const llmResponse = await this.llmService.generateResponse(
        this.sessionState.conversationHistory
      );

      console.log('🤖 LLM Response:', llmResponse.text);

      // Update session state based on metadata
      if (llmResponse.metadata) {
        if (llmResponse.metadata.phase) {
          this.sessionState.currentPhase = llmResponse.metadata.phase;
        }

        // Check if UC was validated
        if (
          llmResponse.text.includes('validei') ||
          llmResponse.text.includes('Perfeito')
        ) {
          this.sessionState.ucValidated = true;
        }
      }

      // Add assistant response to history
      this.sessionState.conversationHistory.push({
        role: 'assistant',
        content: llmResponse.text,
        timestamp: Date.now(),
      });

      // Generate speech
      const audioBuffer = await this.ttsService.textToSpeech(
        llmResponse.text
      );

      // Emit audio to be sent via LiveKit
      this.emit('audio', audioBuffer);

      // Emit transcript for UI
      this.emit('response', {
        text: llmResponse.text,
        metadata: llmResponse.metadata,
      });

    } catch (error) {
      console.error('❌ Error processing user input:', error);
      this.emit('error', error);
    } finally {
      this.isProcessing = false;
    }
  }

  processAudio(audioData: Buffer): void {
    this.sttService.sendAudio(audioData);
  }

  getSessionState(): SessionState {
    return { ...this.sessionState };
  }

  async shutdown(): Promise<void> {
    console.log('🛑 Shutting down voice agent...');
    this.sttService.close();
    this.removeAllListeners();
  }
}

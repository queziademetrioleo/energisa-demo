import { createClient, LiveTranscriptionEvents } from '@deepgram/sdk';
import config from '../config';
import { EventEmitter } from 'events';

export class DeepgramService extends EventEmitter {
  private client;
  private connection: any;

  constructor() {
    super();
    this.client = createClient(config.deepgram.apiKey);
  }

  async startStreaming(): Promise<void> {
    try {
      this.connection = this.client.listen.live({
        model: 'nova-2',
        language: 'pt-BR',
        smart_format: true,
        interim_results: true,
        punctuate: true,
        utterance_end_ms: 1000,
        vad_events: true,
      });

      this.connection.on(LiveTranscriptionEvents.Open, () => {
        console.log('✅ Deepgram connection opened');
        this.emit('ready');
      });

      this.connection.on(LiveTranscriptionEvents.Transcript, (data: any) => {
        const transcript = data.channel?.alternatives?.[0]?.transcript;

        if (transcript && transcript.trim().length > 0) {
          this.emit('transcript', {
            transcript: transcript,
            isFinal: data.is_final || false,
            confidence: data.channel?.alternatives?.[0]?.confidence,
          });
        }
      });

      this.connection.on(LiveTranscriptionEvents.Error, (error: any) => {
        console.error('❌ Deepgram error:', error);
        this.emit('error', error);
      });

      this.connection.on(LiveTranscriptionEvents.Close, () => {
        console.log('🔌 Deepgram connection closed');
        this.emit('close');
      });

    } catch (error) {
      console.error('❌ Failed to start Deepgram streaming:', error);
      throw error;
    }
  }

  sendAudio(audioData: Buffer): void {
    if (this.connection) {
      this.connection.send(audioData);
    }
  }

  close(): void {
    if (this.connection) {
      this.connection.finish();
      this.connection = null;
    }
  }
}

import { ElevenLabsClient } from 'elevenlabs';
import config from '../config';
import { Readable } from 'stream';

export class ElevenLabsService {
  private client: ElevenLabsClient;
  private voiceId: string;

  constructor() {
    this.client = new ElevenLabsClient({
      apiKey: config.elevenlabs.apiKey,
    });
    this.voiceId = config.elevenlabs.voiceId;
  }

  async textToSpeech(text: string): Promise<Buffer> {
    try {
      console.log('🔊 Generating speech for:', text.substring(0, 50) + '...');

      const audioStream = await this.client.textToSpeech.convert(
        this.voiceId,
        {
          text,
          model_id: 'eleven_turbo_v2_5', // Fastest model for real-time
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            style: 0.5,
            use_speaker_boost: true,
          },
          output_format: 'pcm_16000', // 16kHz PCM for LiveKit
        }
      );

      // Convert stream to buffer
      const chunks: Buffer[] = [];

      if (audioStream instanceof Readable) {
        for await (const chunk of audioStream) {
          chunks.push(Buffer.from(chunk));
        }
      } else {
        // If it's already a buffer or array
        chunks.push(Buffer.from(audioStream as any));
      }

      const audioBuffer = Buffer.concat(chunks);
      console.log(`✅ Generated audio: ${audioBuffer.length} bytes`);

      return audioBuffer;
    } catch (error) {
      console.error('❌ ElevenLabs error:', error);
      throw error;
    }
  }

  async textToSpeechStream(text: string): Promise<AsyncIterableIterator<Buffer>> {
    try {
      const audioStream = await this.client.textToSpeech.convert(
        this.voiceId,
        {
          text,
          model_id: 'eleven_turbo_v2_5',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            style: 0.5,
            use_speaker_boost: true,
          },
          output_format: 'pcm_16000',
        }
      );

      // Return async iterator
      async function* streamToAsyncIterator(stream: any): AsyncIterableIterator<Buffer> {
        if (stream instanceof Readable) {
          for await (const chunk of stream) {
            yield Buffer.from(chunk);
          }
        } else {
          yield Buffer.from(stream as any);
        }
      }

      return streamToAsyncIterator(audioStream);
    } catch (error) {
      console.error('❌ ElevenLabs streaming error:', error);
      throw error;
    }
  }
}

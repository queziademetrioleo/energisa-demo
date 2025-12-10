import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

interface Config {
  livekit: {
    url: string;
    apiKey: string;
    apiSecret: string;
  };
  deepgram: {
    apiKey: string;
  };
  google: {
    apiKey: string;
  };
  elevenlabs: {
    apiKey: string;
    voiceId: string;
  };
  server: {
    port: number;
    env: string;
  };
}

const config: Config = {
  livekit: {
    url: process.env.LIVEKIT_URL || 'ws://localhost:7880',
    apiKey: process.env.LIVEKIT_API_KEY || '',
    apiSecret: process.env.LIVEKIT_API_SECRET || '',
  },
  deepgram: {
    apiKey: process.env.DEEPGRAM_API_KEY || '',
  },
  google: {
    apiKey: process.env.GOOGLE_API_KEY || '',
  },
  elevenlabs: {
    apiKey: process.env.ELEVENLABS_API_KEY || '',
    voiceId: process.env.ELEVENLABS_VOICE_ID || '',
  },
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    env: process.env.NODE_ENV || 'development',
  },
};

// Validate required config
export function validateConfig(): void {
  const required = [
    { key: 'LIVEKIT_API_KEY', value: config.livekit.apiKey },
    { key: 'LIVEKIT_API_SECRET', value: config.livekit.apiSecret },
    { key: 'DEEPGRAM_API_KEY', value: config.deepgram.apiKey },
    { key: 'GOOGLE_API_KEY', value: config.google.apiKey },
    { key: 'ELEVENLABS_API_KEY', value: config.elevenlabs.apiKey },
    { key: 'ELEVENLABS_VOICE_ID', value: config.elevenlabs.voiceId },
  ];

  const missing = required.filter(({ value }) => !value);

  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:');
    missing.forEach(({ key }) => console.error(`   - ${key}`));
    console.error('\n📝 Please copy .env.example to .env and fill in the values');
    process.exit(1);
  }
}

export default config;

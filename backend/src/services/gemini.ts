import { GoogleGenerativeAI } from '@google/generative-ai';
import config from '../config';
import { ConversationMessage, LLMResponse } from '../types';
import { GISA_SYSTEM_PROMPT } from '../agent/gisaPrompt';

export class GeminiService {
  private genAI: GoogleGenerativeAI;
  private model: any;

  constructor() {
    this.genAI = new GoogleGenerativeAI(config.google.apiKey);

    // Using Gemini 2.5 Flash - optimized for speed
    this.model = this.genAI.getGenerativeModel({
      model: 'gemini-2.0-flash-exp',
      generationConfig: {
        temperature: 0.7,
        topP: 0.95,
        topK: 40,
        maxOutputTokens: 500, // Keep responses concise for voice
      },
    });
  }

  async generateResponse(
    conversationHistory: ConversationMessage[]
  ): Promise<LLMResponse> {
    try {
      // Build conversation context
      const messages = [
        { role: 'user', parts: [{ text: GISA_SYSTEM_PROMPT }] },
        ...conversationHistory.map((msg) => ({
          role: msg.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: msg.content }],
        })),
      ];

      // Remove system messages and format properly
      const formattedMessages = messages.filter(
        (msg) => msg.role !== 'system'
      );

      const chat = this.model.startChat({
        history: formattedMessages.slice(0, -1),
      });

      const lastMessage = formattedMessages[formattedMessages.length - 1];
      const result = await chat.sendMessage(
        lastMessage.parts[0].text
      );

      const response = await result.response;
      const text = response.text();

      console.log('🤖 Gemini response:', text.substring(0, 100) + '...');

      return {
        text,
        metadata: this.extractMetadata(text),
      };
    } catch (error) {
      console.error('❌ Gemini error:', error);
      throw error;
    }
  }

  private extractMetadata(text: string): any {
    // Extract protocol numbers, phases, etc.
    const metadata: any = {};

    const protocolMatch = text.match(/DEMO-[\w-]+/);
    if (protocolMatch) {
      metadata.protocol = protocolMatch[0];
    }

    if (text.includes('FASE_1') || text.includes('Com quem eu falo')) {
      metadata.phase = 'FASE_1';
    } else if (
      text.includes('Unidade Consumidora') ||
      text.includes('UC')
    ) {
      metadata.phase = 'FASE_2';
    } else {
      metadata.phase = 'FASE_3';
    }

    return metadata;
  }
}

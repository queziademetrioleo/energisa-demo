# 🏗️ Arquitetura do Sistema - GISA Voice Agent

## 📊 Visão Geral

O sistema GISA é uma aplicação de agente de voz em tempo real que integra múltiplos serviços de IA para fornecer um atendimento técnico automatizado via voz.

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Browser                                                │     │
│  │  ┌──────────┐        ┌─────────────┐                  │     │
│  │  │ Microphone│───────▶│ LiveKit SDK │                  │     │
│  │  └──────────┘        └─────────────┘                  │     │
│  │                              │                          │     │
│  │                              ▼                          │     │
│  │                       ┌─────────────┐                  │     │
│  │                       │   WebRTC    │                  │     │
│  │                       │   Stream    │                  │     │
│  │                       └─────────────┘                  │     │
│  │                              │                          │     │
│  └──────────────────────────────┼──────────────────────────┘     │
└─────────────────────────────────┼──────────────────────────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │  LiveKit     │
                          │  Server      │
                          │  (WebRTC)    │
                          └──────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Node.js)                           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              Voice Agent Orchestrator                   │     │
│  │                                                          │     │
│  │  1. Audio In ──▶ 2. STT ──▶ 3. LLM ──▶ 4. TTS ──▶ Audio Out│
│  └────────────────────────────────────────────────────────┘     │
│           │              │           │           │               │
│           ▼              ▼           ▼           ▼               │
│  ┌──────────────┐ ┌──────────┐ ┌─────────┐ ┌──────────────┐   │
│  │   LiveKit    │ │ Deepgram │ │ Gemini  │ │ ElevenLabs   │   │
│  │   Handler    │ │  Nova 3  │ │ 2.5 Flash│ │ Turbo v2.5   │   │
│  │              │ │  (STT)   │ │  (LLM)  │ │    (TTS)     │   │
│  └──────────────┘ └──────────┘ └─────────┘ └──────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                          │           │           │
                          ▼           ▼           ▼
                   ┌──────────────────────────────────┐
                   │      External AI Services         │
                   │  - Deepgram API                   │
                   │  - Google Gemini API              │
                   │  - ElevenLabs API                 │
                   └──────────────────────────────────┘
```

## 🧩 Componentes

### 1. Frontend (React + LiveKit Client)

**Responsabilidades:**
- Capturar áudio do microfone do usuário
- Estabelecer conexão WebRTC via LiveKit
- Reproduzir áudio da resposta do agente
- Exibir transcrições em tempo real

**Tecnologias:**
- React 18
- LiveKit Client SDK
- Web Audio API
- MediaStream API

**Arquivos principais:**
- `frontend/src/App.tsx` - Componente principal
- `frontend/src/index.css` - Estilos

### 2. Backend (Node.js + Express)

**Responsabilidades:**
- Gerenciar sessões de voz
- Orquestrar o fluxo STT → LLM → TTS
- Integrar com serviços de IA
- Gerenciar estado da conversa

**Tecnologias:**
- Node.js 18+
- Express
- TypeScript
- LiveKit Server SDK

**Arquivos principais:**
- `backend/src/index.ts` - Servidor HTTP e API
- `backend/src/agent/voiceAgent.ts` - Orquestrador do agente
- `backend/src/services/` - Integrações com APIs

### 3. LiveKit Server

**Responsabilidades:**
- Gerenciar conexões WebRTC
- Roteamento de áudio em tempo real
- Controle de qualidade (QoS)
- Sincronização de streams

**Configuração:**
- `livekit.yaml` - Configuração do servidor
- Portas: 7880 (WebSocket), 50000-60000 (RTC)

### 4. Serviços de IA

#### Deepgram Nova 3 (STT)
- **Função:** Speech-to-Text
- **Modelo:** nova-3
- **Idioma:** pt-BR
- **Latência:** ~300ms
- **Features:**
  - Streaming transcription
  - VAD (Voice Activity Detection)
  - Punctuation
  - Smart formatting

#### Google Gemini 2.5 Flash (LLM)
- **Função:** Compreensão e geração de linguagem
- **Modelo:** gemini-2.0-flash-exp
- **Contexto:** Até 1M tokens
- **Latência:** ~500ms
- **Features:**
  - Conversational AI
  - Context awareness
  - Multi-turn dialogue

#### ElevenLabs Turbo v2.5 (TTS)
- **Função:** Text-to-Speech
- **Modelo:** eleven_turbo_v2_5
- **Voz:** Configurável
- **Latência:** ~200ms
- **Features:**
  - Natural voice synthesis
  - Portuguese support
  - Streaming audio
  - Voice customization

## 🔐 Segurança

### Autenticação
- Tokens JWT gerados pelo backend
- Validação de chaves API
- Rate limiting (recomendado em produção)

### Comunicação
- WebRTC com DTLS-SRTP
- HTTPS recomendado em produção
- API keys em variáveis de ambiente

### Privacidade
- Áudio não é armazenado por padrão
- Transcrições podem ser descartadas após sessão
- Sem compartilhamento de dados com terceiros

## 📈 Performance

### Latência Total (end-to-end)
- **Audio capture:** ~50ms
- **WebRTC transmission:** ~100ms
- **STT (Deepgram):** ~300ms
- **LLM (Gemini):** ~500ms
- **TTS (ElevenLabs):** ~200ms
- **Audio playback:** ~50ms

**Total aproximado:** 1.2s (aceitável para conversação)

### Otimizações
- Streaming de áudio quando possível
- Cache de respostas comuns (futuro)
- Compressão de áudio (Opus codec)
- WebRTC adaptativo (adaptive bitrate)

## 🔄 Estados do Sistema

### Estados da Conexão
1. **Disconnected** - Sem conexão
2. **Connecting** - Estabelecendo conexão
3. **Connected** - Conectado e pronto

### Estados do Agente
1. **Idle** - Aguardando início
2. **Listening** - Ouvindo o usuário
3. **Thinking** - Processando com LLM
4. **Speaking** - Reproduzindo resposta

### Estados da Conversa
1. **FASE_1** - Saudação inicial
2. **FASE_2** - Validação da UC
3. **FASE_3** - Atendimento técnico

## 📦 Dados de Sessão

```typescript
interface SessionState {
  sessionId: string;
  conversationHistory: ConversationMessage[];
  currentPhase: 'FASE_1' | 'FASE_2' | 'FASE_3';
  ucValidated: boolean;
  ucNumber?: string;
  startTime: number;
}
```

## 🎯 Cenários de Uso

### Fluxo Normal
1. Usuário inicia conversa
2. Frontend solicita token ao backend
3. Frontend conecta ao LiveKit
4. Backend inicia sessão do agente
5. Agente envia saudação inicial
6. Loop de conversa:
   - Usuário fala → STT → LLM → TTS → Resposta
7. Usuário encerra → Cleanup

### Tratamento de Erros
- Reconexão automática (WebRTC)
- Retry de APIs com backoff exponencial
- Fallback para mensagens de erro amigáveis
- Logging estruturado de erros

## 🔧 Escalabilidade

### Horizontal
- Backend stateless (sessões em memória ou Redis)
- Load balancer na frente do backend
- Múltiplas instâncias do LiveKit

### Vertical
- Recursos por sessão: ~100MB RAM
- CPU: ~5-10% por sessão ativa
- Rede: ~50kbps por sessão

### Limites Recomendados
- **Dev:** 5-10 sessões simultâneas
- **Prod (single instance):** 50-100 sessões
- **Prod (cluster):** 1000+ sessões

## 🛠️ Monitoramento

### Métricas Importantes
- Latência end-to-end
- Taxa de erro de APIs
- Sessões ativas
- Uso de recursos (CPU, RAM, rede)
- Qualidade de áudio (MOS score)

### Ferramentas Sugeridas
- Prometheus + Grafana
- ELK Stack (logs)
- Sentry (error tracking)
- LiveKit observability dashboard

## 🚀 Deploy

### Ambientes

**Desenvolvimento:**
- Backend local (localhost:3000)
- Frontend local (localhost:5173)
- LiveKit local (localhost:7880)

**Produção:**
- Backend em servidor/container
- Frontend via CDN (Cloudflare, Vercel)
- LiveKit Cloud ou self-hosted

### Requisitos de Infra
- **Backend:** 2 vCPUs, 4GB RAM
- **LiveKit:** 4 vCPUs, 8GB RAM (para ~100 sessões)
- **Rede:** 100Mbps mínimo

---

Para mais detalhes, consulte os arquivos de código-fonte.

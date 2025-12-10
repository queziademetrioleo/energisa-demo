# 🎙️ GISA - Agente de Voz em Tempo Real

Assistente Inteligente da Energisa especializada em atendimento técnico de falta de energia elétrica.

## 🏗️ Arquitetura

```
[Microfone do Usuário]
        ↓
[LiveKit WebRTC]
        ↓
[Backend Node.js]
        ↓
[Deepgram Nova 3 - STT]
        ↓
[Google Gemini 2.5 Flash - LLM]
        ↓
[ElevenLabs TTS]
        ↓
[LiveKit WebRTC]
        ↓
[Fone do Usuário]
```

## 🚀 Tecnologias

### Backend
- **Node.js** + **TypeScript**
- **LiveKit** - WebRTC para áudio em tempo real
- **Deepgram Nova 3** - Speech-to-Text (STT)
- **Google Gemini 2.5 Flash Lite** - Large Language Model (LLM)
- **ElevenLabs** - Text-to-Speech (TTS)
- **Express** - API REST

### Frontend
- **React** + **TypeScript**
- **Vite** - Build tool
- **LiveKit Client SDK** - WebRTC client
- **CSS moderno** - Interface responsiva

## 📋 Pré-requisitos

### 1. Node.js
```bash
node --version  # v18.0.0 ou superior
npm --version   # v9.0.0 ou superior
```

### 2. LiveKit Server

#### Opção A: Docker (Recomendado)
```bash
docker run -d \
  --name livekit \
  -p 7880:7880 \
  -p 7881:7881 \
  -p 7882:7882/udp \
  -v $PWD/livekit.yaml:/livekit.yaml \
  livekit/livekit-server \
  --config /livekit.yaml
```

#### Opção B: Download Binário
Baixe em: https://github.com/livekit/livekit/releases

### 3. Chaves de API

Você precisará de contas e chaves API para:

- **Deepgram**: https://console.deepgram.com/
- **Google AI Studio**: https://makersuite.google.com/app/apikey
- **ElevenLabs**: https://elevenlabs.io/

## ⚙️ Configuração

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd energisa-demo
```

### 2. Configure o arquivo `.env`
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# LiveKit Configuration
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=sua_api_key_aqui
LIVEKIT_API_SECRET=seu_api_secret_aqui

# Deepgram Configuration (STT)
DEEPGRAM_API_KEY=sua_deepgram_api_key_aqui

# Google Gemini Configuration (LLM)
GOOGLE_API_KEY=sua_google_api_key_aqui

# ElevenLabs Configuration (TTS)
ELEVENLABS_API_KEY=sua_elevenlabs_api_key_aqui
ELEVENLABS_VOICE_ID=seu_voice_id_aqui

# Server Configuration
PORT=3000
NODE_ENV=development
```

### 3. Configure o LiveKit Server

Crie o arquivo `livekit.yaml`:

```yaml
port: 7880
rtc:
  port_range_start: 50000
  port_range_end: 60000
  use_external_ip: false

keys:
  your_api_key: your_api_secret
```

**Importante**: Use a mesma `api_key` e `api_secret` que você colocou no arquivo `.env`.

### 4. Instale as dependências
```bash
npm install
```

Isso instalará as dependências de ambos os workspaces (backend e frontend).

## 🎮 Como Executar

### Desenvolvimento (Backend + Frontend)
```bash
npm run dev
```

Isso iniciará:
- Backend na porta `3000`
- Frontend na porta `5173`

### Apenas Backend
```bash
npm run dev:backend
```

### Apenas Frontend
```bash
npm run dev:frontend
```

## 📱 Como Usar

1. Certifique-se de que o LiveKit Server está rodando
2. Execute o projeto com `npm run dev`
3. Abra o navegador em `http://localhost:5173`
4. Clique em **"Iniciar Conversa"**
5. Permita o acesso ao microfone
6. Comece a falar com a GISA!

## 🎯 Fluxo da Conversa

A GISA segue um fluxo em 3 fases:

### Fase 1: Saudação
> "Olá... Eu sou a Gisa! Assistente Inteligente da Energisa. Com quem eu falo?"

### Fase 2: Validação da UC
> "Para continuar seu atendimento, poderia me informar o número da sua Unidade Consumidora?"

### Fase 3: Atendimento
Classificação em 14 cenários diferentes:
- **Grupo A**: Orientações sem registro
- **Grupo B**: Consultas de situações existentes
- **Grupo C**: Registros de novas ocorrências
- **Grupo D**: Casos especiais

## 🛠️ Estrutura do Projeto

```
energisa-demo/
├── backend/
│   ├── src/
│   │   ├── agent/
│   │   │   ├── gisaPrompt.ts      # Prompt da GISA
│   │   │   └── voiceAgent.ts      # Lógica do agente
│   │   ├── services/
│   │   │   ├── deepgram.ts        # Integração Deepgram
│   │   │   ├── elevenlabs.ts      # Integração ElevenLabs
│   │   │   └── gemini.ts          # Integração Gemini
│   │   ├── config.ts              # Configurações
│   │   ├── types.ts               # Tipos TypeScript
│   │   └── index.ts               # Servidor principal
│   ├── package.json
│   └── tsconfig.json
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # Componente principal
│   │   ├── index.css              # Estilos
│   │   └── main.tsx               # Entry point
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

## 🔧 APIs Disponíveis

### POST `/api/token`
Gera token de acesso para LiveKit
```json
{
  "roomName": "gisa-room-123",
  "participantName": "user-456"
}
```

### POST `/api/session/start`
Inicia uma nova sessão do agente
```json
{
  "sessionId": "session-789",
  "roomName": "gisa-room-123"
}
```

### GET `/api/session/:sessionId`
Consulta status da sessão

### POST `/api/session/:sessionId/end`
Encerra uma sessão

### GET `/health`
Health check do servidor

## 🎨 Customização

### Voz do Agente (ElevenLabs)

Para mudar a voz:
1. Acesse https://elevenlabs.io/voice-library
2. Escolha uma voz
3. Copie o `voice_id`
4. Atualize `ELEVENLABS_VOICE_ID` no `.env`

### Prompt do Agente

Edite o arquivo `backend/src/agent/gisaPrompt.ts` para customizar:
- Personalidade da GISA
- Cenários de atendimento
- Frases padrão
- Regras de negócio

### Interface Visual

Edite `frontend/src/index.css` para customizar:
- Cores
- Layout
- Animações
- Responsividade

## 🐛 Troubleshooting

### Erro: "Failed to connect to LiveKit"
- Verifique se o LiveKit Server está rodando
- Confirme que a porta 7880 está acessível
- Verifique as credenciais no `.env`

### Erro: "Microphone access denied"
- Permita acesso ao microfone no navegador
- Use HTTPS ou localhost (HTTP só funciona em localhost)

### Erro: "API key invalid"
- Verifique todas as chaves de API no `.env`
- Confirme que as chaves estão ativas e com créditos

### Audio não está sendo reproduzido
- Verifique as permissões de áudio do navegador
- Teste com fones de ouvido
- Verifique o volume do sistema

## 📊 Monitoramento

### Logs do Backend
```bash
cd backend
npm run dev
```

Logs disponíveis:
- ✅ Conexões bem-sucedidas
- 🎵 Audio recebido/enviado
- 📝 Transcrições (STT)
- 🤖 Respostas do LLM
- 🔊 Geração de áudio (TTS)
- ❌ Erros e warnings

### Logs do Frontend
Abra o DevTools do navegador (F12) e veja:
- Console: Logs de conexão e eventos
- Network: Requisições HTTP e WebSocket

## 🚀 Deploy em Produção

### Backend
```bash
cd backend
npm run build
npm start
```

### Frontend
```bash
cd frontend
npm run build
```

Os arquivos de produção estarão em `frontend/dist/`.

### Recomendações
- Use HTTPS em produção
- Configure CORS adequadamente
- Use variáveis de ambiente seguras
- Configure rate limiting
- Implemente logging estruturado
- Use um processo manager (PM2, systemd)

## 📝 Licença

Este projeto é privado e proprietário da Energisa.

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de Troubleshooting
2. Consulte a documentação das APIs:
   - LiveKit: https://docs.livekit.io/
   - Deepgram: https://developers.deepgram.com/
   - Google AI: https://ai.google.dev/
   - ElevenLabs: https://elevenlabs.io/docs/

---

Desenvolvido com ❤️ para a Energisa
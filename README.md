# 🐍 GISA - Agente de Voz em Tempo Real (100% Python)

Assistente Inteligente da Energisa especializada em atendimento técnico de falta de energia elétrica.

**🎯 Projeto completamente em Python - Backend FastAPI + Frontend Gradio**

## 🏗️ Arquitetura

```
[Microfone do Usuário]
        ↓
[Interface Gradio (Python)]
        ↓
[Backend FastAPI (Python)]
        ↓
[Deepgram Nova 3 - STT]
        ↓
[Google Gemini 2.0 Flash - LLM]
        ↓
[ElevenLabs Turbo v2.5 - TTS]
        ↓
[Interface Gradio (Python)]
        ↓
[Fone do Usuário]
```

## 🚀 Tecnologias (100% Python!)

### Backend
- **Python 3.10+** - Linguagem principal
- **FastAPI** - Framework web assíncrono moderno
- **Uvicorn** - ASGI server de alta performance
- **Deepgram Nova 3** - Speech-to-Text (STT)
- **Google Gemini 2.0 Flash** - Large Language Model (LLM)
- **ElevenLabs Turbo v2.5** - Text-to-Speech (TTS)
- **Pydantic** - Validação de dados

### Frontend
- **Gradio 4.16** - Interface web interativa (100% Python!)
- **Numpy** - Processamento de áudio
- **SoundFile** - Manipulação de arquivos de áudio

## 📋 Pré-requisitos

### 1. Python
```bash
python --version  # 3.10 ou superior
pip --version     # 23.0 ou superior
```

### 2. Chaves de API

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
# Deepgram Configuration (STT)
DEEPGRAM_API_KEY=sua_deepgram_api_key_aqui

# Google Gemini Configuration (LLM)
GOOGLE_API_KEY=sua_google_api_key_aqui

# ElevenLabs Configuration (TTS)
ELEVENLABS_API_KEY=sua_elevenlabs_api_key_aqui
ELEVENLABS_VOICE_ID=seu_voice_id_aqui

# Server Configuration
PORT=3000
HOST=0.0.0.0
NODE_ENV=development
```

### 3. Instale as dependências

#### Com pip (recomendado para começar)
```bash
pip install -r requirements.txt
```

#### Com Poetry (recomendado para produção)
```bash
poetry install
```

## 🎮 Como Executar

### Opção 1: Executar Tudo de Uma Vez (Simples!)

```bash
# Terminal 1: Backend
cd backend
python -m src.main

# Terminal 2: Frontend Gradio
python app.py
```

### Opção 2: Com Poetry

```bash
# Terminal 1: Backend
cd backend
poetry run python -m src.main

# Terminal 2: Frontend
poetry run python app.py
```

### Acessar a aplicação

- **Frontend Gradio**: http://localhost:7860
- **Backend API**: http://localhost:3000
- **Docs da API**: http://localhost:3000/docs

## 📱 Como Usar

1. **Inicie o backend**
   ```bash
   cd backend && python -m src.main
   ```

2. **Inicie o frontend Gradio**
   ```bash
   python app.py
   ```

3. **Abra o navegador** em `http://localhost:7860`

4. **Clique em "Verificar Backend"** para confirmar que está conectado

5. **Clique em "Iniciar Sessão"**

6. **Grave um áudio** usando o microfone

7. **Ouça a resposta** da GISA!

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

## 🛠️ Estrutura do Projeto (100% Python!)

```
energisa-demo/
├── app.py                     # Frontend Gradio (Python!)
├── requirements.txt           # Dependências Python
├── pyproject.toml             # Poetry config
├── .env.example               # Exemplo de configuração
├── backend/
│   ├── src/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configurações
│   │   ├── models.py          # Modelos Pydantic
│   │   ├── agent/
│   │   │   ├── gisa_prompt.py # Prompt da GISA
│   │   │   └── voice_agent.py # Lógica do agente
│   │   └── services/
│   │       ├── deepgram.py    # STT
│   │       ├── gemini.py      # LLM
│   │       └── elevenlabs.py  # TTS
│   └── requirements.txt
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

Edite o arquivo `backend/src/agent/gisa_prompt.py` para customizar:
- Personalidade da GISA
- Cenários de atendimento
- Frases padrão
- Regras de negócio

### Interface Gradio

Edite `app.py` para customizar:
- Layout da interface
- Cores e tema
- Componentes
- Funcionalidades

## 🐛 Troubleshooting

### Erro: "Backend offline"
```bash
# Inicie o backend primeiro
cd backend
python -m src.main
```

### Erro: "API key invalid"
- Verifique todas as chaves de API no `.env`
- Confirme que as chaves estão ativas e com créditos

### Áudio não está sendo processado
- Verifique as permissões de microfone no navegador
- Teste com fones de ouvido
- Verifique se o backend está rodando

### ModuleNotFoundError
```bash
# Instale as dependências novamente
pip install -r requirements.txt
```

## 📊 Monitoramento

### Logs do Backend
```bash
cd backend
python -m src.main
```

Logs disponíveis:
- ✅ Conexões bem-sucedidas
- 🎵 Audio recebido/enviado
- 📝 Transcrições (STT)
- 🤖 Respostas do LLM
- 🔊 Geração de áudio (TTS)
- ❌ Erros e warnings

### Interface Gradio
Acesse http://localhost:7860 e veja:
- Status da conexão
- Histórico de conversas
- Indicadores visuais de processamento

## 🚀 Deploy em Produção

### Backend
```bash
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 3000
```

Ou com Gunicorn:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

### Frontend Gradio
```bash
python app.py
```

Para deploy em servidor:
```bash
python app.py --server-name 0.0.0.0 --server-port 7860
```

### Recomendações
- Use HTTPS em produção
- Configure variáveis de ambiente seguras
- Use um processo manager (systemd, supervisor)
- Configure firewall adequadamente
- Implemente rate limiting
- Use logs estruturados

## 🎯 Vantagens da Versão 100% Python

### ✅ Por que Python para TUDO?

1. **Desenvolvimento Unificado**
   - Uma única linguagem
   - Mesmo ambiente de desenvolvimento
   - Compartilhamento de código entre backend e frontend

2. **SDKs Superiores**
   - Deepgram, Gemini, ElevenLabs têm SDKs Python melhores
   - Mais documentação e exemplos
   - Comunidade mais ativa em AI/ML

3. **Gradio > React para AI**
   - Interface específica para AI/ML
   - Componentes de áudio nativos
   - Deploy mais simples
   - Zero JavaScript/TypeScript

4. **Manutenção Simplificada**
   - Menos dependências
   - Um package manager (pip/poetry)
   - Debugging mais fácil
   - Stack homogênea

5. **Prototipagem Rápida**
   - Gradio permite iteração rápida
   - Interface bonita automática
   - Menos código boilerplate

## 📝 Licença

Este projeto é privado e proprietário da Energisa.

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de Troubleshooting
2. Consulte a documentação das APIs:
   - Gradio: https://www.gradio.app/docs/
   - FastAPI: https://fastapi.tiangolo.com/
   - Deepgram: https://developers.deepgram.com/
   - Google AI: https://ai.google.dev/
   - ElevenLabs: https://elevenlabs.io/docs/

---

## 🐍 100% Python

Backend: **Python + FastAPI**
Frontend: **Python + Gradio**
AI Services: **Deepgram + Gemini + ElevenLabs**

**Desenvolvido com ❤️ para a Energisa**

# GISA Voice Agent - Backend Python

Backend em Python com FastAPI para o agente de voz GISA.

## 🚀 Tecnologias

- **Python 3.10+**
- **FastAPI** - Framework web assíncrono
- **Uvicorn** - ASGI server
- **LiveKit** - WebRTC
- **Deepgram** - Speech-to-Text
- **Google Gemini** - LLM
- **ElevenLabs** - Text-to-Speech

## 📦 Instalação

### Usando pip

```bash
cd backend
pip install -r requirements.txt
```

### Usando Poetry (recomendado)

```bash
cd backend
poetry install
```

## ⚙️ Configuração

Configure o arquivo `.env` na raiz do projeto com suas chaves de API.

## 🎮 Como Executar

### Com pip

```bash
cd backend
python -m src.main
```

Ou:

```bash
uvicorn src.main:app --reload --port 3000
```

### Com Poetry

```bash
cd backend
poetry run python -m src.main
```

## 📁 Estrutura

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configurações
│   ├── models.py            # Modelos Pydantic
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── gisa_prompt.py   # Prompt da GISA
│   │   └── voice_agent.py   # Agente de voz
│   └── services/
│       ├── __init__.py
│       ├── deepgram.py      # STT
│       ├── gemini.py        # LLM
│       └── elevenlabs.py    # TTS
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 🔧 APIs

- `GET /health` - Health check
- `POST /api/token` - Gera token LiveKit
- `POST /api/session/start` - Inicia sessão
- `GET /api/session/{session_id}` - Status da sessão
- `POST /api/session/{session_id}/end` - Encerra sessão

## 🐛 Debug

Logs são exibidos no console com emojis para fácil identificação:

- ✅ Sucesso
- ❌ Erro
- 🎯 Processamento
- 📝 Transcrição
- 🤖 LLM
- 🔊 TTS

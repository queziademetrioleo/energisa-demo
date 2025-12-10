# 🚀 Quick Start - GISA Voice Agent

Guia rápido para iniciar o projeto em minutos.

## ⚡ Setup Rápido (5 minutos)

### 1. Clone e instale (1 min)
```bash
git clone <seu-repositorio>
cd energisa-demo
npm install
```

### 2. Configure as APIs (2 min)

Copie o `.env.example`:
```bash
cp .env.example .env
```

Edite `.env` e adicione suas chaves:
- **Deepgram**: https://console.deepgram.com/ (Free trial disponível)
- **Google AI**: https://makersuite.google.com/app/apikey (Grátis)
- **ElevenLabs**: https://elevenlabs.io/ (10.000 caracteres grátis/mês)

### 3. Inicie o LiveKit (1 min)

**Com Docker:**
```bash
docker run -d \
  --name livekit \
  -p 7880:7880 \
  -p 7881:7881 \
  -p 7882:7882/udp \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server
```

**Sem Docker:**
- Baixe: https://github.com/livekit/livekit/releases
- Execute: `./livekit-server --dev`

### 4. Execute o projeto (1 min)
```bash
npm run dev
```

### 5. Acesse o app
Abra: http://localhost:5173

Clique em **"Iniciar Conversa"** e comece a falar!

## 🎯 Teste Rápido

1. **Clique em "Iniciar Conversa"**
2. **Permita acesso ao microfone**
3. **GISA diz**: "Olá... Eu sou a Gisa! Com quem eu falo?"
4. **Você responde**: "Oi, sou João"
5. **GISA pergunta**: "Qual o número da sua Unidade Consumidora?"
6. **Você responde**: "1234"
7. **GISA continua**: "Como posso te ajudar?"
8. **Você diz**: "Estou sem luz"

## 🎭 Cenários de Teste

### Falta de Energia Isolada
> "Só a minha casa está sem luz, os vizinhos têm energia"

### Falta de Energia Coletiva
> "A rua inteira está sem luz"

### Problema com Disjuntor
> "O disjuntor fica caindo toda hora"

### Consulta de Protocolo
> "Já tenho protocolo, quanto tempo falta?"

### Iluminação Pública
> "A luz do poste da rua está apagada"

## ❓ Problemas Comuns

### "Failed to connect to LiveKit"
```bash
# Verifique se o LiveKit está rodando
docker ps | grep livekit

# Ou teste manualmente
curl http://localhost:7880
```

### "API key invalid"
- Verifique o arquivo `.env`
- Certifique-se de que copiou as chaves corretamente
- Remova espaços em branco das chaves

### "Microphone access denied"
- Clique no ícone de cadeado na barra de endereço
- Permita acesso ao microfone
- Recarregue a página

## 📊 Verificações

### Backend rodando?
```bash
curl http://localhost:3000/health
# Deve retornar: {"status":"healthy",...}
```

### Frontend rodando?
Abra: http://localhost:5173

### LiveKit rodando?
```bash
curl http://localhost:7880
```

## 🎨 Customização Rápida

### Mudar a voz
1. Vá em https://elevenlabs.io/voice-library
2. Escolha uma voz
3. Copie o `voice_id`
4. Cole em `.env` → `ELEVENLABS_VOICE_ID`
5. Reinicie o backend

### Mudar o prompt
Edite: `backend/src/agent/gisaPrompt.ts`

### Mudar as cores
Edite: `frontend/src/index.css`

## 🎓 Próximos Passos

- Leia o [README.md](README.md) completo
- Explore a estrutura do código
- Customize o prompt da GISA
- Adicione novos cenários
- Implemente analytics

## 💡 Dicas

- Use fones de ouvido para evitar eco
- Fale claramente e pausadamente
- Aguarde a GISA terminar de falar antes de responder
- Teste diferentes cenários
- Verifique os logs do backend para debug

---

**Tudo pronto?** Comece a conversar com a GISA! 🎙️

"""GISA Voice Agent - Interface Gradio (100% Python)."""
import gradio as gr
import requests
import io
import time
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

# Backend URL
BACKEND_URL = "http://localhost:3000"


class GISAInterface:
    """GISA Gradio Interface."""

    def __init__(self):
        """Initialize interface."""
        self.session_id = None
        self.conversation_history = []

    def start_session(self):
        """Start a new session."""
        try:
            self.session_id = f"session-{int(time.time())}"
            room_name = f"gisa-room-{int(time.time())}"

            response = requests.post(
                f"{BACKEND_URL}/api/session/start",
                json={
                    "session_id": self.session_id,
                    "room_name": room_name,
                },
                timeout=10,
            )

            if response.status_code == 200:
                return "✅ Sessão iniciada! Comece a falar..."
            else:
                return f"❌ Erro ao iniciar sessão: {response.text}"

        except Exception as e:
            return f"❌ Erro: {str(e)}"

    def end_session(self):
        """End current session."""
        try:
            if not self.session_id:
                return "⚠️ Nenhuma sessão ativa"

            response = requests.post(
                f"{BACKEND_URL}/api/session/{self.session_id}/end",
                timeout=10,
            )

            self.session_id = None
            self.conversation_history = []

            if response.status_code == 200:
                return "✅ Sessão encerrada"
            else:
                return f"❌ Erro ao encerrar sessão: {response.text}"

        except Exception as e:
            return f"❌ Erro: {str(e)}"

    def process_audio(self, audio_input):
        """Process audio input and return response."""
        if not self.session_id:
            return None, "⚠️ Inicie uma sessão primeiro!", self._format_history()

        try:
            # TODO: Integrate with backend for real-time audio processing
            # For now, return a simulated response

            status = "🎤 Processando áudio... (integração completa em desenvolvimento)"

            return None, status, self._format_history()

        except Exception as e:
            return None, f"❌ Erro: {str(e)}", self._format_history()

    def _format_history(self):
        """Format conversation history for display."""
        if not self.conversation_history:
            return "📝 Nenhuma conversa ainda..."

        formatted = []
        for msg in self.conversation_history:
            role = "👤 Você" if msg["role"] == "user" else "🤖 GISA"
            formatted.append(f"{role}: {msg['content']}")

        return "\n\n".join(formatted)

    def check_backend(self):
        """Check if backend is running."""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"✅ Backend conectado\n📊 Sessões ativas: {data['active_sessions']}"
            else:
                return "❌ Backend não está respondendo"
        except Exception as e:
            return f"❌ Backend offline: {str(e)}\n\n💡 Execute: cd backend && python -m src.main"


def create_interface():
    """Create Gradio interface."""
    gisa = GISAInterface()

    with gr.Blocks(
        title="GISA - Assistente de Voz Energisa",
        theme=gr.themes.Soft(primary_hue="purple"),
    ) as demo:
        gr.Markdown(
            """
            # 🎙️ GISA - Assistente de Voz Energisa

            **Assistente Inteligente para atendimento técnico de falta de energia elétrica**

            ---
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 🎤 Interface de Voz")

                status_box = gr.Textbox(
                    label="Status",
                    value="⚪ Aguardando início...",
                    interactive=False,
                    lines=2,
                )

                with gr.Row():
                    start_btn = gr.Button("▶️ Iniciar Sessão", variant="primary")
                    end_btn = gr.Button("⏹️ Encerrar", variant="stop")
                    check_btn = gr.Button("🔍 Verificar Backend")

                gr.Markdown("### 🎙️ Gravação de Áudio")
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="numpy",
                    label="Fale aqui",
                    streaming=False,
                )

                audio_output = gr.Audio(
                    label="Resposta da GISA",
                    autoplay=True,
                )

            with gr.Column(scale=1):
                gr.Markdown("## 📝 Conversa")
                conversation_box = gr.Textbox(
                    label="Histórico",
                    value="📝 Nenhuma conversa ainda...",
                    interactive=False,
                    lines=20,
                )

        gr.Markdown(
            """
            ---

            ## 📊 Fluxo do Atendimento

            ### Fase 1: Saudação
            GISA se apresenta e pergunta seu nome

            ### Fase 2: Validação UC
            GISA solicita o número da Unidade Consumidora

            ### Fase 3: Atendimento
            Classificação do problema em 14 cenários diferentes

            ---

            ## 🎯 Cenários Suportados

            - **Grupo A:** Orientações sem registro (iluminação pública, disjuntor, etc.)
            - **Grupo B:** Consultas existentes (protocolo, manutenção programada)
            - **Grupo C:** Novos registros (falta isolada, coletiva, VIP)
            - **Grupo D:** Casos especiais (reincidência, custo, etc.)

            ---

            ## 💡 Dicas de Uso

            1. **Inicie uma sessão** antes de falar
            2. **Fale claramente** e aguarde a resposta
            3. **Use fones de ouvido** para evitar eco
            4. **Verifique o backend** se tiver problemas

            ---

            ### 🐍 100% Python
            Backend: FastAPI | Frontend: Gradio | STT: Deepgram | LLM: Gemini | TTS: ElevenLabs
            """
        )

        # Event handlers
        start_btn.click(
            fn=gisa.start_session,
            inputs=[],
            outputs=[status_box],
        )

        end_btn.click(
            fn=gisa.end_session,
            inputs=[],
            outputs=[status_box],
        )

        check_btn.click(
            fn=gisa.check_backend,
            inputs=[],
            outputs=[status_box],
        )

        audio_input.change(
            fn=gisa.process_audio,
            inputs=[audio_input],
            outputs=[audio_output, status_box, conversation_box],
        )

    return demo


if __name__ == "__main__":
    print("")
    print("🎙️  ========================================")
    print("🎙️   GISA - Voice Agent (100% Python)")
    print("🎙️  ========================================")
    print("")
    print("✅ Iniciando interface Gradio...")
    print("📡 Backend deve estar rodando em: http://localhost:3000")
    print("")
    print("💡 Para iniciar o backend:")
    print("   cd backend && python -m src.main")
    print("")

    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )

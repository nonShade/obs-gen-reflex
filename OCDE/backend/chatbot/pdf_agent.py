"""
PDF Chatbot Agent usando Agno framework para OCDE Observatory
Usa Agent + PDFReader + Claude para responder preguntas sobre PDFs
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.knowledge.reader.pdf_reader import PDFReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgnoPDFChatbot:
    """
    Chatbot usando Agno framework con Agent, PDFReader y Claude.
    """

    def __init__(self, pdf_directory: str = "assets/chatbot/"):
        """
        Inicializa el chatbot con Agno.

        Args:
            pdf_directory: Directorio que contiene los archivos PDF
        """
        self.pdf_directory = pdf_directory
        self.agent: Optional[Agent] = None
        self.documents = []
        self._initialize()

    def _initialize(self):
        """Inicializa Agno Agent con PDFReader y Claude."""
        try:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY no configurada")
                return

            self._load_pdf_documents()

            if not self.documents:
                logger.warning("No se encontraron documentos PDF válidos")
                return

            context = self._create_context()

            # Crear Agent con Claude
            self.agent = Agent(
                model=Claude(id="claude-sonnet-4-5"),
                instructions=f"""Eres un asistente inteligente especializado en el Observatorio de Género en Ciencia de la Universidad de La Frontera (UFRO).

CONTEXTO DE DOCUMENTOS:
{context}

REGLAS IMPORTANTES:
1. Solo responde con información que esté explícitamente en los documentos proporcionados
2. Si no encuentras la información en los documentos, di claramente que no tienes esa información
3. Responde siempre en español
4. Sé conciso pero completo
5. Cita el documento específico cuando sea relevante
6. No inventes información que no esté en los documentos""",
                description="Asistente del Observatorio OCDE especializado en documentos PDF",
            )

            logger.info("Agno Agent inicializado correctamente con Claude")

        except Exception as e:
            logger.error(f"Error inicializando Agno Agent: {e}")

    def _load_pdf_documents(self):
        """Carga documentos PDF usando PDFReader de Agno."""
        try:
            if not os.path.exists(self.pdf_directory):
                logger.warning(f"Directorio {self.pdf_directory} no existe")
                return

            pdf_files = list(Path(self.pdf_directory).glob("*.pdf"))
            if not pdf_files:
                logger.warning(
                    f"No se encontraron archivos PDF en {self.pdf_directory}"
                )
                return

            pdf_reader = PDFReader()

            for pdf_file in pdf_files:
                try:
                    logger.info(f"Cargando {pdf_file.name} con Agno PDFReader")
                    documents = pdf_reader.read(str(pdf_file))
                    self.documents.extend(documents)
                except Exception as e:
                    logger.error(f"Error leyendo {pdf_file.name} con Agno: {e}")

            logger.info(
                f"Cargados {len(self.documents)} documentos PDF exitosamente con Agno"
            )

        except Exception as e:
            logger.error(f"Error cargando documentos PDF con Agno: {e}")

    def _create_context(self) -> str:
        """Crea contexto limitado a partir de los documentos."""
        if not self.documents:
            return ""

        context_parts = []
        total_length = 0
        max_context_length = 50000

        for doc in self.documents:
            doc_content = f"\n\n=== DOCUMENTO ===\n{doc.content}\n"
            if total_length + len(doc_content) > max_context_length:
                remaining = max_context_length - total_length
                if remaining > 100:
                    doc_content = doc_content[:remaining] + "...\n[DOCUMENTO TRUNCADO]"
                    context_parts.append(doc_content)
                break

            context_parts.append(doc_content)
            total_length += len(doc_content)

        return "".join(context_parts)

    def is_ready(self) -> bool:
        """Verifica si el agent está listo para responder."""
        return self.agent is not None and len(self.documents) > 0

    def ask(self, question: str) -> str:
        """
        Hace una pregunta al agent usando Agno.

        Args:
            question: Pregunta del usuario

        Returns:
            Respuesta del agent
        """
        try:
            if not self.is_ready():
                return "El chatbot no está disponible. Verifique ANTHROPIC_API_KEY y documentos PDF."

            if not question.strip():
                return "Por favor, haz una pregunta específica sobre los documentos del observatorio."

            if self.agent is not None:
                response = self.agent.run(question)
            else:
                return "El agente no está inicializado correctamente."

            if hasattr(response, "content"):
                return str(response.content)
            else:
                return str(response)

        except Exception as e:
            logger.error(f"Error procesando pregunta con Agno: {e}")
            return f"Error al procesar tu pregunta: {str(e)}"

    def get_available_documents(self) -> List[str]:
        """Obtiene la lista de documentos PDF disponibles."""
        if not os.path.exists(self.pdf_directory):
            return []
        return [f.name for f in Path(self.pdf_directory).glob("*.pdf")]

    def get_agent_info(self) -> Dict[str, Any]:
        """Obtiene información sobre el estado del agent."""
        return {
            "ready": self.is_ready(),
            "pdf_directory": self.pdf_directory,
            "available_documents": self.get_available_documents(),
            "model": "Claude Sonnet 4.5 (via Agno)",
            "documents_loaded": len(self.documents),
            "framework": "Agno",
            "uses_pdf_reader": True,
            "uses_semantic_search": False,
        }

agno_chatbot = AgnoPDFChatbot()

def get_pdf_chatbot_response(question: str) -> str:
    """Función de utilidad para obtener respuesta del chatbot Agno."""
    return agno_chatbot.ask(question)

def is_pdf_chatbot_ready() -> bool:
    """Función de utilidad para verificar si el chatbot Agno está listo."""
    return agno_chatbot.is_ready()

def get_pdf_chatbot_info() -> Dict[str, Any]:
    """Función de utilidad para obtener información del chatbot Agno."""
    return agno_chatbot.get_agent_info()

if __name__ == "__main__":
    print("=== PDF Chatbot con Agno Framework ===")
    print("Información del chatbot:")
    info = get_pdf_chatbot_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    if is_pdf_chatbot_ready():
        print("\n¡Chatbot Agno listo! Puedes hacer preguntas.")

        # Pregunta de prueba
        test_question = "¿Qué información hay disponible sobre el observatorio?"
        print(f"\nPregunta de prueba: {test_question}")
        response = get_pdf_chatbot_response(test_question)
        print(f"Respuesta: {response[:200]}...")
    else:
        print("\nChatbot Agno no está listo. Verifica la configuración.")

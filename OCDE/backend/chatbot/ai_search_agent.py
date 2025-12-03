import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.models.anthropic import Claude

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgnoSearchAgent:
    """
    AI Search Agent usando Agno framework para búsqueda inteligente.
    """

    def __init__(self, data_directory: str = "./"):
        """
        Inicializa el agente de búsqueda con Agno.

        Args:
            data_directory: Directorio que contiene los archivos de datos CSV/Excel
        """
        self.data_directory = data_directory
        self.agent: Optional[Agent] = None
        self.investigadores_data = []
        self.all_areas = []
        self.investigadores_summary = ""
        self._initialize()

    def _initialize(self):
        """Inicializa Agno Agent con Claude."""
        try:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY no configurada")
                return

            self._load_data()

            if not self.investigadores_data:
                logger.warning("No se encontraron datos de investigadores válidos")
                return

            self._create_agent()

            logger.info("Agno Search Agent inicializado correctamente")

        except Exception as e:
            logger.error(f"Error inicializando Agno Search Agent: {e}")

    def _load_data(self):
        """Carga y procesa datos de investigadores, publicaciones y proyectos."""
        try:
            # Cargar datos de investigadores
            academicas_file = os.path.join(self.data_directory, "academicas.xlsx")
            publicaciones_file = os.path.join(
                self.data_directory, "publicaciones___.csv"
            )
            proyectos_file = os.path.join(
                self.data_directory, "proyectos_total_ocde1_.csv"
            )

            if not os.path.exists(academicas_file):
                logger.error(f"Archivo {academicas_file} no encontrado")
                return

            # Procesar investigadores
            df_academicas = pd.read_excel(academicas_file)
            df_academicas = df_academicas.replace("", None)
            df_academicas["id"] = pd.to_numeric(df_academicas["id"], errors="coerce")
            df_academicas = df_academicas.dropna(subset=["id"])
            df_academicas["id"] = df_academicas["id"].astype(int)
            df_academicas["orcid"] = df_academicas["orcid"].fillna("")
            df_academicas["grado_mayor"] = (
                df_academicas["grado_mayor"].astype(str).replace("nan", "INVESTIGADORA")
            )
            df_academicas["ocde_2"] = (
                df_academicas["ocde_2"]
                .astype(str)
                .apply(lambda x: ", ".join(x.split("#")) if x and x != "nan" else "")
            )

            publicaciones_data = []
            proyectos_data = []

            if os.path.exists(publicaciones_file):
                df_pub = pd.read_csv(publicaciones_file, encoding="utf-8-sig")
                publicaciones_data = df_pub.to_dict("records")

            if os.path.exists(proyectos_file):
                df_proy = pd.read_csv(proyectos_file, encoding="utf-8-sig")
                proyectos_data = df_proy.to_dict("records")

            self._create_investigators_summary_extended(
                df_academicas, publicaciones_data, proyectos_data
            )

            self.all_areas = sorted(
                df_academicas["ocde_2"]
                .dropna()
                .str.split(",")
                .explode()
                .str.strip()
                .unique()
                .tolist()
            )

            # Convertir a lista de diccionarios
            self.investigadores_data = df_academicas.to_dict("records")

            logger.info(
                f"Cargados {len(self.investigadores_data)} investigadores, {len(publicaciones_data)} publicaciones, {len(proyectos_data)} proyectos y {len(self.all_areas)} áreas"
            )

        except Exception as e:
            logger.error(f"Error cargando datos: {e}")

    def _create_investigators_summary_extended(
        self, df: pd.DataFrame, publicaciones_data: list, proyectos_data: list
    ):
        """Crea un resumen extendido de investigadores incluyendo títulos de publicaciones y proyectos."""
        try:
            area_counts = {}
            investigator_details = []

            pub_by_rut = {}
            proy_by_rut = {}

            for pub in publicaciones_data:
                rut = pub.get("rut_ir")
                if rut:
                    if rut not in pub_by_rut:
                        pub_by_rut[rut] = []
                    pub_by_rut[rut].append(pub)

            for proy in proyectos_data:
                rut = proy.get("rut_ir")
                if rut:
                    if rut not in proy_by_rut:
                        proy_by_rut[rut] = []
                    proy_by_rut[rut].append(proy)

            for _, inv in df.head(
                30
            ).iterrows():
                areas_str = inv.get("ocde_2", "")
                if areas_str and areas_str != "nan":
                    areas = areas_str.split(",")
                else:
                    areas = []
                areas = [area.strip() for area in areas if area.strip()]

                for area in areas:
                    area_counts[area] = area_counts.get(area, 0) + 1

                # Obtener publicaciones y proyectos del investigador
                rut = inv.get("rut_ir")
                publicaciones = pub_by_rut.get(rut, [])
                proyectos = proy_by_rut.get(rut, [])

                pub_titles = [
                    pub.get("titulo", "")[:100] for pub in publicaciones[:3]
                ]  # Primeros 3
                proy_titles = [
                    proy.get("titulo", "")[:100] for proy in proyectos[:3]
                ]  # Primeros 3

                inv_detail = f"- {inv['name']} (ID: {inv['id']}, RUT: {rut}, Áreas: {inv.get('ocde_2', 'N/A')})"
                if pub_titles:
                    inv_detail += f"\n  Publicaciones: {'; '.join(pub_titles)}"
                if proy_titles:
                    inv_detail += f"\n  Proyectos: {'; '.join(proy_titles)}"

                investigator_details.append(inv_detail)

            self.investigadores_summary = f"""
RESUMEN EXTENDIDO DE INVESTIGADORES CON PUBLICACIONES Y PROYECTOS:

ÁREAS OCDE PRINCIPALES:
{", ".join([f"{area} ({count})" for area, count in sorted(area_counts.items(), key=lambda x: x[1], reverse=True)[:15]])}

INVESTIGADORES CON SUS TRABAJOS:
{chr(10).join(investigator_details[:15])}

TOTAL DE INVESTIGADORES: {len(df)}
TOTAL DE ÁREAS: {len(self.all_areas)}
TOTAL DE PUBLICACIONES: {len(publicaciones_data)}
TOTAL DE PROYECTOS: {len(proyectos_data)}

INSTRUCCIONES PARA BÚSQUEDA POR TÍTULOS:
- Si el usuario menciona un título de publicación o proyecto específico, busca en los títulos mostrados arriba
- Si encuentras coincidencia parcial en título, devuelve el nombre del investigador asociado
- Ejemplo: "VALIDACION DE ESCALA SOLEDAD" → Alba Zambrano Constanzo
"""

        except Exception as e:
            logger.error(f"Error creando resumen extendido de investigadores: {e}")
            self.investigadores_summary = (
                "Error cargando resumen extendido de investigadores"
            )

    def _create_agent(self):
        """Crea el agente Agno."""
        try:
            self.agent = Agent(
                model=Claude(id="claude-sonnet-4-5"),
                instructions=f"""Eres un asistente inteligente especializado en búsqueda de investigadoras del Observatorio de Género en Ciencia de la Universidad de La Frontera (UFRO).

INFORMACIÓN DE INVESTIGADORES CON PUBLICACIONES Y PROYECTOS:
{self.investigadores_summary}

ÁREAS OCDE COMPLETAS DISPONIBLES: {", ".join(self.all_areas)}

TU TAREA:
1. Analizar consultas de búsqueda en lenguaje natural sobre investigadoras y sus trabajos
2. DETECTAR AUTOMÁTICAMENTE si la consulta busca:
   - NOMBRES DE PERSONAS (ej: "Alba Zambrano", "María García", "Dr. López")
   - ÁREAS DE INVESTIGACIÓN (ej: "matemáticas", "biotecnología", "psicología")
   - TÍTULOS DE TRABAJOS (ej: "validación escala soledad", "células madre", nombres de proyectos)
   - CONSULTAS HÍBRIDAS (ej: "María García matemáticas", "Alba Zambrano psicología")
3. Responder SOLO en formato JSON como se especifica abajo

FORMATO DE RESPUESTA REQUERIDO (siempre JSON válido):
{{
    "tipo_busqueda": "nombre|area|titulo|hibrida",
    "areas_detectadas": ["área1", "área2"],
    "nombres_detectados": ["nombre1", "nombre2"],
    "titulos_detectados": ["fragmento_titulo1", "fragmento_titulo2"],
    "terminos_busqueda": ["término1", "término2"],
    "resumen": "breve explicación de los resultados encontrados"
}}

REGLAS PARA DETECCIÓN AUTOMÁTICA:
- tipo_busqueda "nombre": Si detectas nombres propios como "Alba Zambrano", "María", "Dr. López"
- tipo_busqueda "area": Si detectas disciplinas/campos como "matemáticas", "biotecnología", "psicología"
- tipo_busqueda "titulo": Si detectas títulos o fragmentos de publicaciones/proyectos
- tipo_busqueda "hibrida": Si detectas COMBINACIÓN de nombres Y áreas O títulos
- Las áreas_detectadas DEBEN ser exactamente de la lista disponible de áreas OCDE
- Los nombres_detectados son nombres de personas mencionados en la consulta
- Los titulos_detectados son fragmentos de títulos de publicaciones/proyectos mencionados
- Los terminos_busqueda son palabras clave generales para búsqueda complementaria
- Máximo 5 áreas detectadas, 3 nombres detectados, 3 títulos detectados, y 5 términos de búsqueda
- Responder SIEMPRE en JSON válido, sin texto adicional
- Si no encuentras nombres, áreas o títulos relevantes, devolver arrays vacíos pero mantener el formato JSON
- Priorizar precisión sobre cantidad de resultados

EJEMPLOS DE DETECCIÓN:
- "Alba Zambrano" → tipo_busqueda: "nombre", nombres_detectados: ["Alba Zambrano"]
- "biotecnología" → tipo_busqueda: "area", areas_detectadas: ["BIOTECNOLOGIA..."]
- "validación escala soledad" → tipo_busqueda: "titulo", titulos_detectados: ["validación escala soledad"]
- "María García matemáticas" → tipo_busqueda: "hibrida", nombres_detectados: ["María García"], areas_detectadas: ["MATEMATICAS"]
- "VALIDACION DE ESCALA SOLEDAD SOCIAL" → tipo_busqueda: "titulo", titulos_detectados: ["VALIDACION DE ESCALA SOLEDAD SOCIAL"]""",
                description="Agente de búsqueda inteligente para investigadoras OCDE",
                markdown=False,
            )

            logger.info("Agno Agent creado exitosamente")

        except Exception as e:
            logger.error(f"Error creando agent: {e}")

    def search(self, query: str) -> Dict[str, Any]:
        """
        Realiza búsqueda inteligente usando el agente.

        Args:
            query: Consulta en lenguaje natural

        Returns:
            Dict con resultados estructurados
        """
        try:
            if not self.agent:
                return self._fallback_search(query)

            if not query.strip():
                return {"error": "Consulta vacía"}

            response = self.agent.run(query)

            if hasattr(response, "content"):
                response_text = str(response.content)
            else:
                response_text = str(response)

            return self._parse_agent_response(response_text)

        except Exception as e:
            logger.error(f"Error en búsqueda inteligente: {e}")
            return self._fallback_search(query)

    def _parse_agent_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea la respuesta JSON del agente."""
        try:
            import json

            start = response_text.find("{")
            end = response_text.rfind("}") + 1

            if start != -1 and end != 0:
                json_str = response_text[start:end]
                data = json.loads(json_str)

                required_keys = [
                    "tipo_busqueda",
                    "areas_detectadas",
                    "nombres_detectados",
                    "terminos_busqueda",
                    "resumen",
                ]
                if all(key in data for key in required_keys):
                    valid_areas = [
                        area
                        for area in data["areas_detectadas"]
                        if area in self.all_areas
                    ]
                    data["areas_detectadas"] = valid_areas
                    return data
                else:
                    old_format_keys = [
                        "areas_detectadas",
                        "terminos_busqueda",
                        "resumen",
                    ]
                    if all(key in data for key in old_format_keys):
                        return {
                            "tipo_busqueda": "area",
                            "areas_detectadas": [
                                area
                                for area in data["areas_detectadas"]
                                if area in self.all_areas
                            ],
                            "nombres_detectados": [],
                            "terminos_busqueda": data["terminos_busqueda"],
                            "resumen": data["resumen"],
                        }

            return self._fallback_search_response(response_text)

        except Exception as e:
            logger.error(f"Error parseando respuesta del agente: {e}")
            return self._fallback_search_response(response_text)

    def _fallback_search(self, query: str) -> Dict[str, Any]:
        """Búsqueda de respaldo cuando el agente no está disponible."""
        try:
            query_lower = query.lower()

            detected_areas = []
            for area in self.all_areas:
                if any(word in area.lower() for word in query_lower.split()):
                    detected_areas.append(area)

            search_terms = [word for word in query_lower.split() if len(word) > 2]

            return {
                "areas_detectadas": detected_areas[:5],  # Limitar a 5
                "terminos_busqueda": search_terms[:5],  # Limitar a 5
                "resumen": f"Búsqueda simple por '{query}'. {len(detected_areas)} áreas relacionadas detectadas.",
            }

        except Exception as e:
            logger.error(f"Error en búsqueda de respaldo: {e}")
            return {
                "areas_detectadas": [],
                "terminos_busqueda": [],
                "resumen": f"Error en la búsqueda: {str(e)}",
            }

    def _fallback_search_response(self, response_text: str) -> Dict[str, Any]:
        """Crear respuesta estructurada cuando el parsing JSON falla."""
        return {
            "areas_detectadas": [],
            "terminos_busqueda": [],
            "resumen": "La búsqueda devolvió resultados pero no en el formato esperado. Intenta reformular tu consulta.",
        }

    def is_ready(self) -> bool:
        """Verifica si el agente está listo."""
        return self.agent is not None and len(self.investigadores_data) > 0

    def get_agent_info(self) -> Dict[str, Any]:
        """Obtiene información sobre el estado del agente."""
        return {
            "ready": self.is_ready(),
            "investigadores_loaded": len(self.investigadores_data),
            "areas_available": len(self.all_areas),
            "model": "Claude Sonnet 4.5 (via Agno)",
            "framework": "Agno (simplified)",
            "uses_vector_search": False,
            "data_directory": self.data_directory,
        }

search_agent = AgnoSearchAgent()

def get_ai_search_response(query: str) -> Dict[str, Any]:
    """Función de utilidad para búsqueda inteligente."""
    return search_agent.search(query)


def is_ai_search_ready() -> bool:
    """Función de utilidad para verificar si el agente está listo."""
    return search_agent.is_ready()


def get_ai_search_info() -> Dict[str, Any]:
    """Función de utilidad para obtener información del agente."""
    return search_agent.get_agent_info()


def get_available_areas() -> List[str]:
    """Función de utilidad para obtener áreas disponibles."""
    return search_agent.all_areas


if __name__ == "__main__":
    print("=== AI Search Agent con Agno Framework (Simplified) ===")
    print("Información del agente:")
    info = get_ai_search_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    if is_ai_search_ready():
        print("\n¡Agente de búsqueda listo!")

        # Pruebas
        test_queries = [
            "busca investigadoras de matemáticas",
            "encuentra expertas en biotecnología",
            "María García publicaciones sobre células",
        ]

        for query in test_queries:
            print(f"\nConsulta: {query}")
            result = get_ai_search_response(query)
            print(f"Áreas detectadas: {result.get('areas_detectadas', [])}")
            print(f"Términos de búsqueda: {result.get('terminos_busqueda', [])}")
            print(f"Resumen: {result.get('resumen', 'Sin resumen')[:100]}...")
    else:
        print("\nAgente de búsqueda no está listo. Verifica la configuración.")

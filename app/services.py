from openai import OpenAI
import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar OpenAI - manejar caso cuando no hay API key
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "test_key_for_demo":
        client = OpenAI(api_key=api_key)
        print(
            f"✅ OpenAI client configurado correctamente (API Key: {api_key[:20]}...)"
        )
    else:
        client = None
        print("⚠️ No se encontró API key válida de OpenAI")
except Exception as e:
    client = None
    print(f"❌ Error al configurar cliente OpenAI: {e}")


def analizar_con_ia(descripcion: str, tipo_servicio: str) -> Optional[Dict]:
    """
    Analiza la descripción del caso con IA de OpenAI

    Args:
        descripcion: Descripción del caso legal proporcionada por el cliente
        tipo_servicio: Tipo de servicio solicitado

    Returns:
        Dict con análisis de complejidad, ajuste de precio, servicios adicionales y propuesta profesional
    """

    print(f"🔍 Analizando caso con IA:")
    print(f"   - Descripción: {descripcion[:50]}...")
    print(f"   - Tipo de servicio: {tipo_servicio}")
    print(f"   - Cliente OpenAI disponible: {client is not None}")
    print(f"   - API Key presente: {os.getenv('OPENAI_API_KEY') is not None}")

    if not client or not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Usando datos simulados - no hay cliente OpenAI válido")
        # Retornar datos simulados si no hay API key válida
        return {
            "complejidad": "Media",
            "ajuste_precio": 25,
            "servicios_adicionales": [
                "Análisis de documentos",
                "Consulta especializada",
            ],
            "propuesta_texto": f"Estimado cliente, hemos analizado su caso de {tipo_servicio}: '{descripcion[:100]}...' y consideramos que requiere un enfoque profesional. Nuestro equipo legal especializado está preparado para brindarle el mejor servicio.",
        }

    print("🤖 Llamando a OpenAI API...")

    prompt = f"""
    Analiza este caso legal: {descripcion}
    Tipo de servicio: {tipo_servicio}
    
    Evalúa:
    1. Complejidad (Baja/Media/Alta)
    2. Ajuste de precio recomendado (0%, 25%, 50%)
    3. Servicios adicionales necesarios
    4. Genera propuesta profesional para cliente

    Responde ÚNICAMENTE en el siguiente formato JSON:
    {{
        "complejidad": "Baja|Media|Alta",
        "ajuste_precio": 0,
        "servicios_adicionales": ["servicio1", "servicio2"],
        "propuesta_texto": "Propuesta profesional aquí..."
    }}
    """

    try:
        # Llamada a API de IA
        print("📡 Enviando request a OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente especializado en análisis legal. Responde únicamente en formato JSON válido.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()
        print(f"✅ Respuesta de OpenAI recibida: {content[:100]}...")

        # Intentar parsear el JSON
        try:
            resultado = json.loads(content)
            print("✅ JSON parseado correctamente")

            # Validar que tenga los campos requeridos
            required_fields = [
                "complejidad",
                "ajuste_precio",
                "servicios_adicionales",
                "propuesta_texto",
            ]
            if all(field in resultado for field in required_fields):
                print("✅ Todos los campos requeridos presentes")
                return resultado
            else:
                print("⚠️ Faltan campos requeridos, usando valores por defecto")
                # Si faltan campos, retornar valores por defecto
                return {
                    "complejidad": "Media",
                    "ajuste_precio": 25,
                    "servicios_adicionales": ["Análisis detallado del caso"],
                    "propuesta_texto": "Estimado cliente, hemos analizado su caso y procedemos con la cotización solicitada.",
                }

        except json.JSONDecodeError as je:
            print(f"❌ Error parseando JSON: {je}")
            # Si no se puede parsear el JSON, intentar extraer información básica
            return {
                "complejidad": "Media",
                "ajuste_precio": 0,
                "servicios_adicionales": ["Consulta especializada"],
                "propuesta_texto": (
                    content[:500] if content else "Análisis completado."
                ),
            }

    except Exception as e:
        print(f"❌ Error en llamada a OpenAI: {e}")
        # Si hay cualquier error con la API, retornar análisis simulado
        return {
            "complejidad": "Media",
            "ajuste_precio": 25,
            "servicios_adicionales": ["Análisis de caso", "Consulta legal"],
            "propuesta_texto": f"Estimado cliente, hemos realizado un análisis preliminar de su caso y estamos listos para brindarle nuestros servicios profesionales.",
        }


def calcular_ajuste_precio(complejidad: str, precio_base: float) -> float:
    """
    Calcula el ajuste de precio basado en la complejidad

    Args:
        complejidad: Nivel de complejidad del caso
        precio_base: Precio base del servicio

    Returns:
        float: Monto del ajuste
    """
    ajustes = {
        "Baja": -0.1,  # 10% descuento
        "Media": 0.0,  # Sin ajuste
        "Alta": 0.25,  # 25% incremento
    }

    factor = ajustes.get(complejidad, 0.0)
    return precio_base * factor

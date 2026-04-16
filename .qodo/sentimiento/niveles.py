import json
from .cliente import client

def analizar_sentimiento_basico(texto: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Analiza el sentimiento. Responde SOLO: positivo, negativo o neutral."},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    return {
        "nivel": "básico",
        "sentimiento": response.choices[0].message.content.strip(),
        "texto_original": texto[:100]
    }

def analizar_sentimiento_intermedio(texto: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento. Responde ÚNICAMENTE en JSON con:
            - sentimiento: positivo, negativo o neutral
            - polaridad: número entre -1 y +1
            - emociones: objeto con puntuaciones (alegria, tristeza, enojo, sorpresa, miedo)
            - intensidad: baja, media, alta
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        resultado = json.loads(response.choices[0].message.content)
        resultado["nivel"] = "intermedio"
        resultado["texto_original"] = texto[:100]
        return resultado
    except:
        return {
            "nivel": "intermedio",
            "error": "Error de parseo",
            "respuesta_raw": response.choices[0].message.content
        }

def analizar_sentimiento_avanzado(texto: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """
            Analiza profundidad. Responde ÚNICAMENTE en JSON con:
            - sentimiento_global: positivo, negativo o neutral
            - polaridad: número entre -1 y +1
            - fragmentos: lista de objetos (texto, sentimiento_individual)
            - justificacion: explicación
            - tonalidad: formal, coloquial, etc.
            - recomendacion: acción a tomar
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        resultado = json.loads(response.choices[0].message.content)
        resultado["nivel"] = "avanzado"
        resultado["texto_original"] = texto[:100]
        return resultado
    except:
        return {
            "nivel": "avanzado",
            "error": "Error de parseo",
            "respuesta_raw": response.choices[0].message.content
        }
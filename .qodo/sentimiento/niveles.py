import json
from .cliente import client

def limpiar_respuesta_json(texto_raw: str) -> str:
    limpio = texto_raw.strip()
    if limpio.startswith("```"):
        lineas = limpio.splitlines()
        if lineas[0].startswith("```"):
            lineas = lineas[1:]
        if lineas and lineas[-1].startswith("```"):
            lineas = lineas[:-1]
        limpio = "\n".join(lineas).strip()
    return limpio

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
            {"role": "system", "content": "Analiza sentimiento. Responde ÚNICAMENTE JSON: sentimiento, polaridad, emociones, intensidad."}
        ],
        temperature=0.0
    )
    
    contenido_raw = response.choices[0].message.content
    try:
        json_limpio = limpiar_respuesta_json(contenido_raw)
        resultado = json.loads(json_limpio)
        resultado["nivel"] = "intermedio"
        resultado["texto_original"] = texto[:100]
        return resultado
    except:
        return {"nivel": "intermedio", "error": "Error de parseo", "respuesta_raw": contenido_raw}

def analizar_sentimiento_avanzado(texto: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Analiza profundidad. Responde ÚNICAMENTE JSON: sentimiento_global, polaridad, fragmentos, justificacion, tonalidad, recomendacion."},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    contenido_raw = response.choices[0].message.content
    try:
        json_limpio = limpiar_respuesta_json(contenido_raw)
        resultado = json.loads(json_limpio)
        resultado["nivel"] = "avanzado"
        resultado["texto_original"] = texto[:100]
        return resultado
    except:
        return {"nivel": "avanzado", "error": "Error de parseo", "respuesta_raw": contenido_raw}
    
from .niveles import analizar_sentimiento_intermedio

def analizar_sentimiento_multitexto(textos: list) -> dict:
    resultados = []
    for texto in textos:
        resultado = analizar_sentimiento_intermedio(texto)
        resultados.append(resultado)
    
    polaridades = [r.get("polaridad", 0) for r in resultados if isinstance(r.get("polaridad"), (int, float))]
    
    estadisticas = {
        "total": len(resultados),
        "positivos": sum(1 for r in resultados if r.get("sentimiento") == "positivo"),
        "negativos": sum(1 for r in resultados if r.get("sentimiento") == "negativo"),
        "neutrales": sum(1 for r in resultados if r.get("sentimiento") == "neutral"),
        "polaridad_promedio": sum(polaridades) / len(polaridades) if polaridades else 0
    }
    
    return {
        "resultados_individuales": resultados,
        "estadisticas": estadisticas
    }
    
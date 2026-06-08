import httpx

# Configuración del modelo y host de Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

def generate_response(question: str, context_chunks: list[str]) -> str:
    """
    Envía la pregunta y los fragmentos relevantes a Ollama.
    """
    context_text = "\n\n---\n\n".join(context_chunks)
    
    if not context_chunks:
        return "No encontré esa información en los documentos cargados."
        
    system_prompt = (
        "Eres un asistente útil que responde preguntas EXCLUSIVAMENTE basándose en la información proporcionada en el contexto. "
        "Si la respuesta no se encuentra en el contexto, debes responder: 'No encontré esa información en los documentos cargados.' "
        "No inventes información, no asumas cosas fuera de lo provisto."
    )
    
    prompt = f"Contexto:\n{context_text}\n\nPregunta: {question}\nRespuesta:"
    
    payload = {
        "model": OLLAMA_MODEL,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }
    
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=60.0)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Error al extraer respuesta del modelo.")
    except Exception as e:
        return f"Error al comunicarse con el modelo Ollama: {str(e)}"

import fitz  # PyMuPDF
import re

def process_document(file_path: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Lee un documento (PDF o TXT) y lo divide en fragmentos (chunks) superpuestos.
    """
    text = ""
    if file_path.lower().endswith(".pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
    # Limpieza básica
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Dividir en chunks
    words = text.split(" ")
    chunks = []
    
    if not words:
        return []
        
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
        
    return chunks

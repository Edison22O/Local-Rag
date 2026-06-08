import chromadb
from chromadb.utils import embedding_functions
import hashlib
import os

# Inicializar ChromaDB en la carpeta local 'data'
client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "data"))

# Usar FastEmbed por defecto (se descarga automáticamente la primera vez)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Obtener o crear la colección principal
collection = client.get_or_create_collection(name="local_rag_docs", embedding_function=embedding_fn)

def index_document(chunks: list[str], filename: str):
    """
    Convierte los fragmentos de texto en vectores y los guarda en ChromaDB.
    """
    if not chunks:
        return
        
    ids = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{filename}_{i}_{chunk}".encode()).hexdigest()
        ids.append(chunk_id)
        metadatas.append({"source": filename, "chunk_index": i})
        
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

def search_documents(query: str, top_k: int = 3) -> list[str]:
    """
    Busca los fragmentos más relevantes en la base vectorial dada una pregunta.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    if not results or not results['documents'] or len(results['documents'][0]) == 0:
        return []
        
    return results['documents'][0]

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil

from src.document_processor import process_document
from src.rag_engine import index_document, search_documents
from src.llm_service import generate_response

app = FastAPI(title="Local Rag Lite")

# Directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. Extraer texto
        chunks = process_document(file_path)
        
        # 2. Indexar texto en base de datos vectorial
        index_document(chunks, file.filename)
        
        return {"status": "success", "message": f"Archivo '{file.filename}' indexado correctamente.", "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    try:
        # 1. Buscar fragmentos relevantes en la base vectorial
        relevant_chunks = search_documents(request.message, top_k=3)
        
        # 2. Generar la respuesta usando el modelo 3b
        response = generate_response(request.message, relevant_chunks)
        
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)

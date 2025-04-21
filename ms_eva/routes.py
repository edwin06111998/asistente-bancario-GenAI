#   Archivo util si se ejecuta el proyecto desde run_ms_eva.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ms_eva.services.UtilService import *
from ms_eva.services.GraphService import *
from ms_eva.services.VectorStoreFEService import *
from ms_eva.db.serviceDb import crear_base_de_datos

router = APIRouter()

class ProcessRequest(BaseModel):
    sessionId: str
    query: str

@router.post("/ms_eva/message")
async def process(request: ProcessRequest):
    try:
        response = processQuery(request.query, request.sessionId)
        save_redis_history(request.query, response["data"], request.sessionId)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
@router.post("/ms_eva/clearHistory")
async def process(request: ProcessRequest):
    try:        
        clear_redis_history(request.sessionId)
        clear_state(request.sessionId)
        return "Historial limpio"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
@router.post("/ms_eva/loadEmbedding")
async def process():
    try:        
        loadEmbedding()
        return "Embedding cargado"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
@router.post("/ms_eva/createDatabase")
async def process():
    try:        
        crear_base_de_datos()
        return "Base de datos cargada"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")
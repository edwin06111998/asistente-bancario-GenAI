from fastapi import FastAPI
from ms_eva.routes import router as client_router

app = FastAPI(title="EVA Service")
app.include_router(client_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
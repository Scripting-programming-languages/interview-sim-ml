from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Interview Simulator API", version="1.0.0")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "ML Interview Service running"}
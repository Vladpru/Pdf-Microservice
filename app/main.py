from fastapi import FastAPI
from app.routers import generate, download

app = FastAPI(title="PDF Service")

app.include_router(generate.router)
app.include_router(download.router)


@app.get("/health")
def health():
    return {"status": "ok"}

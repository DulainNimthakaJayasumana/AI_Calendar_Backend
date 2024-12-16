from fastapi import FastAPI
from app.database import Base, engine
from app.routes import events, ocr, auth

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(events.router)
app.include_router(ocr.router)
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI Calendar API is running"}

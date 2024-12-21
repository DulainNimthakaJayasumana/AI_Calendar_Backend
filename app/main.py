# from fastapi import FastAPI
# from app.database import Base, engine
# from app.routes import events, ocr, auth

# # Create DB tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(events.router)
# app.include_router(ocr.router)
# app.include_router(auth.router)

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

# @app.get("/")
# def root():
#     return {"message": "AI Calendar API is running"}

# #

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import events, ocr, auth

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# CORS middleware (optional, useful for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers for different routes
app.include_router(events.router)
app.include_router(ocr.router)
app.include_router(auth.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI Calendar API is running"}

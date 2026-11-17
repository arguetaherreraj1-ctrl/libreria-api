from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, editoriales, libros

# Crea las tablas automáticamente en la BD al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST - Librería Chiapas",
    description="Proyecto Final Taller de Desarrollo III. Gestión de libros y editoriales con autenticación Bearer Token.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(editoriales.router)
app.include_router(libros.router)

@app.get("/", tags=["General"])
def inicio():
    return {
        "mensaje": "Bienvenido a la API REST de Librería Chiapas",
        "documentacion": "/docs"
    }

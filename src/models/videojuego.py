from datetime import date
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Videojuego(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=100)
    fecha_lanzamiento: date | None = Field(nullable=True)
    genero: str = Field(index = True,max_length=50)
    plataforma: str | None = Field(default=None, max_length=50)

# Clases DTO

class VideojuegoCreate(BaseModel):
    nombre: str
    fecha_lanzamiento: date | None = None
    genero: str
    plataforma: str | None = None

class VideojuegoUpdate(BaseModel):
    nombre: str | None = None
    fecha_lanzamiento: date | None = None
    genero: str | None = None
    plataforma: str | None = None

class VideojuegoResponse(BaseModel):
    id: int
    nombre: str
    fecha_lanzamiento: date | None = None
    genero: str
    plataforma: str | None = None

# Funciones de mapeo entre modelos

def map_videojuego_to_response(videojuego: Videojuego) -> VideojuegoResponse:
    return VideojuegoResponse(
        id=videojuego.id,
        nombre=videojuego.nombre,
        fecha_lanzamiento=videojuego.fecha_lanzamiento,
        genero=videojuego.genero,
        plataforma=videojuego.plataforma
    )

def map_create_to_videojuego(videojuego_create: VideojuegoCreate) -> Videojuego:
    return Videojuego(
        nombre=videojuego_create.nombre,
        fecha_lanzamiento=videojuego_create.fecha_lanzamiento,
        genero=videojuego_create.genero,
        plataforma=videojuego_create.plataforma
    )

def map_update_to_videojuego(videojuego: Videojuego, videojuego_update: VideojuegoUpdate) -> Videojuego:
    if videojuego_update.nombre is not None:
        videojuego.nombre = videojuego_update.nombre
    if videojuego_update.fecha_lanzamiento is not None:
        videojuego.fecha_lanzamiento = videojuego_update.fecha_lanzamiento
    if videojuego_update.genero is not None:
        videojuego.genero = videojuego_update.genero
    if videojuego_update.plataforma is not None:
        videojuego.plataforma = videojuego_update.plataforma
    return videojuego
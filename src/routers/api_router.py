from fastapi import APIRouter, HTTPException
from models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse, map_create_to_videojuego, map_videojuego_to_response
from data.videojuego_repository import VideojuegoRepository
from data.db import SessionDep

router = APIRouter(prefix="/api/videojuegos", tags=["videojuegos"])

# Rutas para la API de videojuegos

@router.get("/", response_model=list[VideojuegoResponse])
def lista_videojuegos(session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuegos = repo.get_all_videojuego()
    return videojuegos

@router.post("/", response_model=VideojuegoResponse)
def nuevo_videojuego(videojuego_created: VideojuegoCreate, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego = map_create_to_videojuego(videojuego_created)
    videojuego_creado = repo.create_videojuego(videojuego)
    return map_videojuego_to_response(videojuego_creado)

@router.get("/{videojuego_id}", response_model=VideojuegoResponse)
def videojuego_por_id(videojuego_id: int, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return map_videojuego_to_response(videojuego_encontrado)

@router.delete("/{videojuego_id}")
def borrar_videojuego(videojuego_id: int, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    repo.delete_videojuego(videojuego_encontrado)
    return {"mensaje": "Videojuego eliminado"}

@router.patch("/{videojuego_id}", response_model=Videojuego)
def cambiar_videojuego(videojuego_id: int, videojuego: Videojuego, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    videojuego_data = videojuego.model_dump(exclude_unset=True)
    videojuego_encontrado.sqlmodel_update(videojuego_data)
    repo.update_videojuego(videojuego_encontrado.id, videojuego_data)
    return videojuego_encontrado

@router.put("/", response_model=Videojuego)
def cambiar_videojuego(videojuego: Videojuego, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego.id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    videojuego_data = videojuego.model_dump()
    videojuego_encontrado.sqlmodel_update(videojuego_data)
    repo.update_videojuego(videojuego_encontrado.id, videojuego_data)
    return videojuego_encontrado

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Annotated

from src.models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse, map_create_to_videojuego, map_videojuego_to_response
from src.data.videojuego_repository import VideojuegoRepository
from src.data.db import get_session, init_db

router = APIRouter(prefix="/api/videojuegos", tags=["videojuegos"])

SessionDep = Annotated[Session, Depends(get_session)]

# Rutas para la API de videojuegos

@router.get("/", response_model=list[VideojuegoResponse])
async def lista_videojuegos(session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuegos = repo.get_all_videojuego()
    return [map_videojuego_to_response(videojuego) for videojuego in videojuegos]

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

@router.delete("/{videojuego_id}", status_code=204)
def borrar_videojuego(videojuego_id: int, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    repo.delete_videojuego(videojuego_encontrado)
    return None

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

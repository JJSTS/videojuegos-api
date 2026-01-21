from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlmodel import Session, select

from src.data.db import get_session, init_db
from src.models.videojuego import Videojuego, VideojuegoCreate, VideojuegoResponse, map_create_to_videojuego, map_videojuego_to_response
from src.data.videojuego_repository import VideojuegoRepository
from src.routers.api_router import router as api_videojuegos_router

import uvicorn

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

app.include_router(api_videojuegos_router)

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/videojuegos", response_class=HTMLResponse)
async def ver_videojuegos(request: Request, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuegos = repo.get_all_videojuego()
    return templates.TemplateResponse("videojuegos/videojuegos.html", {"request": request, "videojuegos": videojuegos})

@app.get("/videojuegos/new", response_class=HTMLResponse)
async def nuevo_videojuego_form(request: Request):
    return templates.TemplateResponse("videojuegos/nuevo_videojuego.html", {
        "request": request,
        "videojuego" : Videojuego()
    })

@app.post("/videojuegos/new", response_class=HTMLResponse)
async def crear_videojuego(request: Request, session: SessionDep):
    form_data = await request.form()
    nombre = form_data.get("nombre")
    genero = form_data.get("genero")
    fecha_lanzamiento = form_data.get("fecha_lanzamiento") or None
    plataforma = form_data.get("plataforma")

    videojuego_create = VideojuegoCreate(
        nombre=nombre,
        genero=genero,
        fecha_lanzamiento=fecha_lanzamiento,
        plataforma=plataforma
    )

    repo = VideojuegoRepository(session)
    videojuego = map_create_to_videojuego(videojuego_create)
    repo.create_videojuego(videojuego)

    return RedirectResponse(url="/videojuegos", status_code=303)

@app.get("/videojuegos/{videojuego_id}", response_class=HTMLResponse)
async def videojuego_por_id(request: Request, videojuego_id: int, session: SessionDep): 
    repo = VideojuegoRepository(session)
    videojuego_encontrado = repo.get_videojuego(videojuego_id)
    if not videojuego_encontrado:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    videojuego_response = map_videojuego_to_response(videojuego_encontrado)
    return templates.TemplateResponse("videojuegos/videojuego_detalle.html", {"request": request, "videojuego": videojuego_response})
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
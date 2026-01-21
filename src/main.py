from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from src.data.db import get_session, init_db
from src.models.videojuego import Videojuego, VideojuegoCreate, map_create_to_videojuego, map_videojuego_to_response
from src.data.videojuego_repository import VideojuegoRepository

import uvicorn

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static.html")
templates = Jinja2Templates(directory="src/templates")

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("videojuegos/index.html", {"request": request})

@app.get("/videojuegos", response_class=HTMLResponse)
async def ver_videojuegos(request: Request, session: SessionDep):
    repo = VideojuegoRepository(session)
    videojuegos = repo.get_all_videojuego()
    return templates.TemplateResponse("videojuegos/videojuegos.html", {"request": request, "videojuegos": videojuegos})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
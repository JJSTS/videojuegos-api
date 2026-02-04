from sqlmodel import Session, select
from src.models.videojuego import Videojuego

class VideojuegoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_videojuego(self) -> list[Videojuego]:
        videojuegos = self.session.exec(select(Videojuego)).all()
        return videojuegos

    def get_videojuego(self, videojuego_id: int) -> Videojuego:
        videojuego = self.session.get(Videojuego, videojuego_id)
        return videojuego

    def create_videojuego(self, videojuego: Videojuego) -> Videojuego:
        self.session.add(videojuego)
        self.session.commit()
        self.session.refresh(videojuego)
        return videojuego

    def update_videojuego(self, videojuego_id: int, videojuego_data: dict) -> Videojuego:
        videojuego = self.get_videojuego(videojuego_id)
        for key, value in videojuego_data.items():
            setattr(videojuego, key, value)
        self.session.commit()
        self.session.refresh(videojuego)
        return videojuego

    def delete_videojuego(self, videojuego_id: int) -> None:
        videojuego = self.get_videojuego(videojuego_id)
        self.session.delete(videojuego)
        self.session.commit()
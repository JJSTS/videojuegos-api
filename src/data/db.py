from dotenv import load_dotenv
from models.videojuego import Videojuego
from sqlmodel import create_engine, SQLModel, Session
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    db_user: str = os.getenv("DB_USER","jjsts")
    db_password: str = os.getenv("DB_PASSWORD","1234")
    db_server: str = os.getenv("DB_SERVER","fastapi-db")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_name: str = os.getenv("DB_NAME","videojuegosdb")
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"

else:
    print("Using DATABASE_URL from environment")

    
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Videojuego(id=1, nombre="The Legend of Zelda: Breath of the Wild", fecha_lanzamiento="2017-03-03", genero="Action-adventure", plataforma="Nintendo Switch"))
        session.add(Videojuego(id=2, nombre="Marvel Rivals", fecha_lanzamiento="2024-11-27", genero="Fighting", plataforma="PC"))
        session.add(Videojuego(id=3, nombre="Minecraft", fecha_lanzamiento="2011-11-18", genero="Sandbox", plataforma="PC"))
        session.add(Videojuego(id=4, nombre="Among Us", fecha_lanzamiento="2018-06-15", genero="Party", plataforma="PC/Mobile"))
        session.commit()

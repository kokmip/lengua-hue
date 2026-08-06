from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass
def init_db():
    from src.database.models import Word
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
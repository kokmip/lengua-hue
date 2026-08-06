from src.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    lemma: Mapped[str] = mapped_column(index=True)
    context: Mapped[str]
    explanation: Mapped[str]
    translation: Mapped[str]
    example_sentence: Mapped[str]
    example_translation: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
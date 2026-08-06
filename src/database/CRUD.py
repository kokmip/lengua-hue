from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database.models import Word
def create_word(db: Session, word: str, lemma: str, context: str, explanation: str, translation: str, example_sentence: str, example_translation: str):
    db_word = Word(word=word, lemma=lemma, context=context, explanation=explanation, translation=translation, example_sentence=example_sentence, example_translation=example_translation)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word
def get_word_by_lemma(db: Session, lemma):
    stmt = select(Word).where(Word.lemma == lemma)
    return db.scalars(stmt).first()
def get_all_words(db: Session):
    stmt = select(Word).order_by(Word.created_at.desc())
    return db.scalars(stmt).all()
def get_word_by_lemma_and_context(db, lemma, context):
    db.query(Word).filter(Word.lemma == lemma, Word.context == context).first()
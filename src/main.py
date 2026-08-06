from src.nlp.european import EuropeanAnalyzer
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session 
from src.database.connection import SessionLocal, init_db
from contextlib import asynccontextmanager
from src.database.CRUD import create_word, get_all_words, get_word_by_lemma_and_context
from src.services.llm import LLMService
class AnalyzeRequest(BaseModel):
    text: str
    lang_code: str = "en"
analyzers = {
    "es" : EuropeanAnalyzer(lang_code="es"),
    "en" : EuropeanAnalyzer(lang_code="en")
}
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield 
app = FastAPI(title="LenguaHUe", lifespan=lifespan)
@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    analyzer = analyzers.get(request.lang_code)
    if not analyzer:
        raise HTTPException(
            status_code=400,
            detail="Selected language is not supported."
        )
    
    tokens = analyzer.analyze(request.text)
    return {
        "language": request.lang_code,
        "tokens": tokens
    }
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class TranslateRequest(BaseModel):
    word: str
    lemma: str
    context: str
    target_lang: str = "ru"
@app.post("/translate")
async def translate_word(request: TranslateRequest, db: Session = Depends(get_db)):
    existing_word = get_word_by_lemma_and_context(db, request.lemma, request.context)
    if existing_word != None:
        return existing_word
    else:
        llm_service = LLMService()
        llm_result = await llm_service.get_contextual_translation(
            word=request.word,
            lemma=request.lemma,
            context=request.context,
            target_lang=request.target_lang
        )
        saved_word = create_word(
            db=db,
            word=request.word,
            lemma=request.lemma,
            context=request.context,
            explanation=llm_result["explanation"],
            translation=llm_result["translation"],
            example_sentence=llm_result["example_sentence"],
            example_translation=llm_result["example_translation"]
        )
        return saved_word
@app.get("/words")
def read_all_words(db: Session = Depends(get_db)):
    return get_all_words(db)
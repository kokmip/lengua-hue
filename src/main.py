from src.nlp.european import EuropeanAnalyzer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI(title="LenguaHUe")
class AnalyzeRequest(BaseModel):
    text: str
    lang_code: str = "en"
analyzers = {
    "es" : EuropeanAnalyzer(lang_code="es"),
    "en" : EuropeanAnalyzer(lang_code="en")
}
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
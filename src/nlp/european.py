import spacy
from wordfreq import zipf_frequency
class EuropeanAnalyzer:
    def __init__(self, lang_code: str):
        if lang_code == "es":
            self.nlp = spacy.load("es_core_news_sm")
        if lang_code == "en":
            self.nlp = spacy.load("en_core_web_sm")
        self.lang_code = lang_code
    def _zipf_to_cefr(self, score: float) -> str:
        if score >= 5:
            return('A1')
        elif score >= 4.2:
            return('A2')
        elif score >= 3.5:
            return('B1')
        elif score >= 2.8:
            return('B2')
        else:
            return('C1/C2')
    def analyze(self, text:str) -> list[dict]:
        doc = self.nlp(text)
        results = []
        for token in doc:
            if not token.is_space and not token.is_punct:
                lemma = token.lemma_.lower()
                zipf = zipf_frequency(lemma, self.lang_code)
                cefr = self._zipf_to_cefr(zipf)
                results.append({
                    "word" : token.text,
                    "lemma" : lemma,
                    "cefr" : cefr,
                    "zipf" : zipf,
                    "sentence": token.sent.text.strip()
                })
        return results

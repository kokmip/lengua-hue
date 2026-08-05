from src.nlp.european import EuropeanAnalyzer 
analyzer = EuropeanAnalyzer(lang_code="es")
data = analyzer.analyze("Los estudiantes hablan sobre sus cosas")
for item in data:
    print(item)
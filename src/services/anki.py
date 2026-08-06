import genanki
import tempfile
qfmt_html = """
<div class="card-container">
    <div class="word-title">{{Word}}</div>
    <div class="context-box">
        "{{Context}}"
    </div>
</div>
"""

afmt_html = """
<div class="card-container">
    <div class="word-title">{{Word}}</div>
    <div class="context-box">
        "{{Context}}"
    </div>
    
    <hr class="divider">
    
    <div class="translation-badge">{{Translation}}</div>
    <div class="lemma-tag">lemma: {{Lemma}}</div>
    
    <div class="info-card">
        <div class="info-header">
            <span>EXPLANATION</span>
        </div>
        <div class="info-text">{{Explanation}}</div>
    </div>
    
    <div class="info-card example-card">
        <div class="info-header">
            <span>EXAMPLE</span>
        </div>
        <div class="example-src">{{Example}}</div>
        <div class="example-tr">{{ExampleTranslation}}</div>
    </div>
</div>
"""

css_style = """
:root {
    --bg-main: #f8fafc;
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --text-subtle: #94a3b8;
    --accent-primary: #6366f1;
    --success-bg: #ecfdf5;
    --success-text: #047857;
    --highlight-bg: #faf5ff;
    --highlight-border: #f3e8ff;
    --highlight-text: #7e22ce;
    --border-color: #e2e8f0;
    --radius-lg: 20px;
    --radius-md: 12px;
    --radius-full: 9999px;
}

.card {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 24px 12px;
    box-sizing: border-box;
}

.card-container {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 32px 26px;
    max-width: 440px;
    width: 100%;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.03), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
    border: 1px solid var(--border-color);
    text-align: center;
    box-sizing: border-box;
}

/* Header Word */
.word-title {
    font-size: 32px;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.02em;
    margin-bottom: 16px;
    line-height: 1.1;
}

/* Context Quote */
.context-box {
    background-color: #f1f5f9;
    color: #334155;
    font-size: 14px;
    line-height: 1.6;
    padding: 12px 16px;
    border-radius: var(--radius-md);
    font-style: italic;
    border-left: 4px solid var(--accent-primary);
    text-align: left;
}

/* Soft Divider */
.divider {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 22px 0;
}

/* Translation Pill */
.translation-badge {
    display: inline-block;
    background-color: var(--success-bg);
    color: var(--success-text);
    font-size: 20px;
    font-weight: 700;
    padding: 6px 20px;
    border-radius: var(--radius-full);
    margin-bottom: 4px;
    box-shadow: 0 2px 4px rgba(4, 120, 87, 0.04);
}

.lemma-tag {
    font-size: 11px;
    color: var(--text-subtle);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 18px;
}

/* Cards & Information */
.info-card {
    background-color: #f8fafc;
    border-radius: var(--radius-md);
    padding: 14px 16px;
    text-align: left;
    margin-bottom: 10px;
    border: 1px solid var(--border-color);
}

.example-card {
    background-color: var(--highlight-bg);
    border-color: var(--highlight-border);
}

.info-header {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    font-weight: 700;
    margin-bottom: 6px;
}

.example-card .info-header {
    color: var(--highlight-text);
}

.info-text {
    font-size: 13px;
    line-height: 1.5;
    color: #334155;
}

.example-src {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 2px;
    line-height: 1.4;
}

.example-tr {
    font-size: 13px;
    color: var(--highlight-text);
    font-style: italic;
}
"""
def generate_anki_deck(words: list):
    anki_model = genanki.Model(
        model_id=1103770778, 
        name="LenguaHue Model",
        fields= [
            {"name": "Word"},
            {"name": "Lemma"},
            {"name": "Translation"},
            {"name": "Context"},
            {"name": "Explanation"},
            {"name": "Example"},
            {"name": "ExampleTranslation"},
        ],
        templates=[{
            "name": "Card",
            "qfmt": qfmt_html,
            "afmt": afmt_html
        }],
        css=css_style
    )
    anki_deck = genanki.Deck(deck_id=1105271117, name="LenguaHue Deck")
    for w in words:
        anki_note = genanki.Note(
            model=anki_model,
            fields= [
                str(w.word or ''),
                str(w.lemma or ''),
                str(w.translation or ''),
                str(w.context or ''),
                str(w.explanation or ''),
                str(w.example_sentence or ''),
                str(w.example_translation or '')
        ]
        )
        anki_deck.add_note(anki_note)
    temp_file = tempfile.NamedTemporaryFile(suffix=".apkg", delete=False)
    genanki.Package(anki_deck).write_to_file(temp_file.name)
    return temp_file.name
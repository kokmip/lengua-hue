import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="LenguaHue", page_icon="📚", layout="wide")
st.title("📚 LenguaHue: Smart Reading and Vocabulary")

tab_reader, tab_vocab = st.tabs(
    ["Reading", "My Glossary"]
)
def send_translation_request(word: str, lemma: str, context: str):
  payload = {
      "word": word,
      "lemma": lemma,
      "context": context,
      "target_lang": "ru",
  }
  response = requests.post(f"{API_URL}/translate", json=payload)
  return response.json()
with tab_vocab:
  st.header("Saved Words")
  if st.button("Reload"):
    res = requests.get(f"{API_URL}/words")
    if res.status_code == 200:
      words = res.json()
      for word in words:
        with st.expander(f"📌 {word['word']} ({word['lemma']}) — {word['translation']}"):
          st.write(f"**Context:** {word['context']}")
          st.write(f"**Explanation:** {word['explanation']}")
          st.write(f"**Example:** {word['example_sentence']}")
          st.write(f"**Translation of example:** {word['example_translation']}")
with tab_reader:
  st.header("📖 Анализ текста")

  # Поле ввода текста
  text_input = st.text_area(
      "Вставьте текст для чтения:",
      "Ella cree que el queso es delicioso.",
  )
  lang = st.selectbox("Язык текста:", ["es", "en"])

  # Кнопка анализа
  if st.button("Разобрать текст"):
    res = requests.post(
        f"{API_URL}/analyze", json={"text": text_input, "lang_code": lang}
    )
    if res.status_code == 200:
      # Сохраняем токены в состояние сессии
      st.session_state["tokens"] = res.json()["tokens"]

  # Если токены уже есть в памяти сессии, показываем форму перевода
  if "tokens" in st.session_state and st.session_state["tokens"]:
    st.divider()
    st.subheader("Выберите слово для перевода:")

    # Формируем список отображаемых слов
    word_options = [
        f"{t['text']} (лемма: {t['lemma']})" for t in st.session_state["tokens"]
    ]
    selected_option = st.selectbox("Слово из текста:", word_options)

    # Достаем выбранный объект токена
    selected_index = word_options.index(selected_option)
    token_data = st.session_state["tokens"][selected_index]

    if st.button("✨ Перевести и сохранить в словарь"):
      payload = {
          "word": token_data["text"],
          "lemma": token_data["lemma"],
          "context": text_input,  # Весь текст или предложение в качестве контекста
          "target_lang": "ru",
      }
      trans_res = requests.post(f"{API_URL}/translate", json=payload)
      if trans_res.status_code == 200:
        st.success(
            f"Слово '{token_data['lemma']}' успешно добавлено в словарь!"
        )
      else:
        st.error("Ошибка при переводе слова.")
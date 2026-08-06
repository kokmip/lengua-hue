import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="LenguaHue", layout="wide")
st.title("LenguaHue")

tab_reader, tab_vocab = st.tabs(["Text Analysis", "Vocabulary"])

with tab_reader:
    st.header("Text Analysis")

    text_input = st.text_area(
        "Enter text to analyze:",
        "Ella cree que el queso es delicioso."
    )
    lang = st.selectbox("Text language:", ["es", "en"])

    if st.button("Analyze Text"):
        response = requests.post(
            f"{API_URL}/analyze", json={"text": text_input, "lang_code": lang}
        )
        if response.status_code == 200:
            st.session_state["tokens"] = response.json()["tokens"]
        else:
            st.error("Failed to analyze text.")

    if "tokens" in st.session_state and st.session_state["tokens"]:
        st.divider()
        st.subheader("Select a word to translate:")

        word_options = []
        for t in st.session_state["tokens"]:
            if isinstance(t, dict):
                word_str = t.get("word") or t.get("text") or "N/A"
                lemma_str = t.get("lemma", word_str)
                word_options.append(f"{word_str} (lemma: {lemma_str})")
            else:
                word_options.append(str(t))

        selected_option = st.selectbox("Word from text:", word_options)
        selected_index = word_options.index(selected_option)
        token_data = st.session_state["tokens"][selected_index]

        if st.button("Translate and Save"):
            if isinstance(token_data, dict):
                word_val = token_data.get("word") or token_data.get("text")
                lemma_val = token_data.get("lemma", word_val)
            else:
                word_val = str(token_data)
                lemma_val = str(token_data)

            payload = {
                "word": word_val,
                "lemma": lemma_val,
                "context": token_data.get("sentence", text_input),
                "target_lang": "ru"
            }
            trans_res = requests.post(f"{API_URL}/translate", json=payload)
            if trans_res.status_code == 200:
                st.success(f"Word '{lemma_val}' added to vocabulary.")
            else:
                st.error("Failed to translate word.")

with tab_vocab:
    st.header("Vocabulary")
    if st.button("Refresh"):
        res = requests.get(f"{API_URL}/words")
        if res.status_code == 200:
            st.session_state["words"] = res.json()
        else:
            st.error("Failed to load vocabulary.")

    words = st.session_state.get("words", [])
    if not words:
        res = requests.get(f"{API_URL}/words")
        if res.status_code == 200:
            words = res.json()
            st.session_state["words"] = words

    for word in words:
        with st.expander(f"{word.get('word')} ({word.get('lemma')}) - {word.get('translation')}"):
            st.write(f"**Context:** {word.get('context')}")
            st.write(f"**Explanation:** {word.get('explanation')}")
            st.write(f"**Example:** {word.get('example_sentence')}")
            st.write(f"**Example Translation:** {word.get('example_translation')}")
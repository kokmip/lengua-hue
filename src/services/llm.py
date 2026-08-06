import os 
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
class LLMService:
    def __init__ (self, model_name: str = "openrouter/free"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=self.api_key,
    )
        self.model_name = model_name
    async def get_contextual_translation(self, word: str, lemma: str, context: str, target_lang: str = "ru") -> dict:
        prompt = f"""You are professional linguist with 20 years experience. Your entry data is word: {word}, lemma: {lemma}, context: {context}
        and your goal is make a JSON-object with next keys: 
        1. translation: the excact translation of lemma for this context in {target_lang}
        2. explanation: a short explanation of meaning (1 sentence) in the original language of this word
        3. example_sentence: new simple sentence in original language
        4. example_translation: translation of the new sentence in {target_lang}"""
        try:
            response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
      )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {
            "translation": lemma,
            "explanation": "Unsuccessful attempt.",
            "example_sentence": "",
            "example_translation": "",
            "error": str(e)
        }
if __name__ == "__main__":
  llm = LLMService()
  res = llm.get_contextual_translation(
      word="hablan",
      lemma="hablar",
      context="Los estudiantes hablan español.",
      target_lang="ru",
  )
  print(json.dumps(res, ensure_ascii=False, indent=2))
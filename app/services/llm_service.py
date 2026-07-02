import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


class LLMService:

    def __init__(self):
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate(self, prompt):
        try:
            response = self.model.generate_content(prompt)

            print("\n===== GEMINI RAW RESPONSE =====")
            print(response)
            print("===============================\n")

            print("Response text:")
            print(response.text)

            return response.text

        except Exception as e:
            print("Gemini Error:", e)
            return ""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    #set up connection to open AI API using .env file
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OPENAI_API_KEY in environment file.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    #define chat function
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM API error: {e}")
            return None

import json
from .prompt_manager import SYSTEM_PROMPT, CLASSIFICATION_PROMPT

class EmailClassifier:
    def __init__(self, llm_client):
        self.llm = llm_client

    def classify(self, email_text: str) -> dict:
        prompt = CLASSIFICATION_PROMPT.format(email_text=email_text)
        result = self.llm.chat(SYSTEM_PROMPT, prompt)
        try:
            return json.loads(result)
        except Exception:
            return {"error": "Failed to parse LLM response", "raw_output": result}

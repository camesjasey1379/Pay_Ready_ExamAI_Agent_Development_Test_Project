from .prompt_manager import RESPONSE_PROMPT

class EmailResponder:
    def __init__(self, llm_client):
        self.llm = llm_client

    def generate_response(self, classification, sentiment, urgency, main_issue):
        prompt = RESPONSE_PROMPT.format(
            classification=classification,
            sentiment=sentiment,
            urgency=urgency,
            main_issue=main_issue
        )
        return self.llm.chat("You are a helpful support agent.", prompt)

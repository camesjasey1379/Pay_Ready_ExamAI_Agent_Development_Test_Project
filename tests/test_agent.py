from agent.classifier import EmailClassifier
from agent.llm_client import LLMClient

def test_basic_classification():
    llm = LLMClient()
    classifier = EmailClassifier(llm)
    email_text = "I can't access my account."
    result = classifier.classify(email_text)
    assert "classification" in result

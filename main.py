import json
from agent.llm_client import LLMClient
from agent.classifier import EmailClassifier
from agent.responder import EmailResponder

def process_email(email_text: str):
    llm = LLMClient()
    classifier = EmailClassifier(llm)
    responder = EmailResponder(llm)

    classification_data = classifier.classify(email_text)
    if "error" in classification_data:
        return classification_data

    response = responder.generate_response(
        classification_data["classification"],
        classification_data["sentiment"],
        classification_data["urgency"],
        classification_data["main_issue"]
    )

    classification_data["response_template"] = response
    return classification_data


if __name__ == "__main__":
    print("Paste or type your customer support email below. End input with an empty line:\n")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    email_text = "\n".join(lines)

    result = process_email(email_text)
    print("\n=== RESULT JSON ===")
    print(json.dumps(result, indent=2))

import json
from agent.llm_client import LLMClient
from agent.classifier import EmailClassifier
from agent.responder import EmailResponder

#Agent coordinator that triggers distinct workflow steps
def process_email(email_text: str, mode = "AB"):


    llm = LLMClient()
    classifier = EmailClassifier(llm,mode=mode)
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

    print("Select classification mode:")
    print("A  - Use Prompt A only")
    print("B  - Use Prompt B only")
    print("AB - Run full A/B evaluation (self-reflect)")
    mode = input("Enter mode (A/B/AB): ").strip().upper() or "AB"
    print(f"DEBUG: Mode selected = {mode}")


    print("Paste or type your customer support email below. End input with an empty line:\n")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    email_text = "\n".join(lines)

    result = process_email(email_text,mode=mode)
    print("=== RESULT JSON ===")
    print(json.dumps(result, indent=2))

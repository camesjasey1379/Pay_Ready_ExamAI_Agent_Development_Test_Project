import json
from .prompt_manager import (
    SYSTEM_PROMPT,
    CLASSIFICATION_PROMPT_A,
    CLASSIFICATION_PROMPT_B,
    EVALUATION_PROMPT
)

class EmailClassifier:
    
    
    def __init__(self, llm_client):
        self.llm = llm_client
    #utilizes a classification prompt and returns parsed json or error info
    def classify_with_prompt(self,prompt_template,email_text):
        prompt = prompt_template.format(email_text=email_text)
        result = self.llm.chat(SYSTEM_PROMPT,prompt)
        try:
            parsed = json.loads(result)
            valid = True
        except Exception:
            parsed = {"error": "Invalid JSON","raw_output": result}
            valid = False
        return parsed, valid, result
    
    #evaluate the versions of the response A + B and determine which is more accurate
    def evaluate_versions(self, email_text, output_a, output_b):
        eval_prompt = EVALUATION_PROMPT.format(
            email_text = email_text,
            output_a = json.dumps(output_a, indent=2),
            output_b =json.dumps(output_b,indent=2),
        )
        eval_result = self.llm.chat("You are a fair and strict Evaluator", eval_prompt)
        try:
            return json.loads(eval_result)
        except Exception:
            return {"winner": "A", "reasoning": "Evaluation failed, defaulted to A."}
        
    def classify(self,email_text: str):
        #print process steps
        print("\n Running classification prompt A")
        output_a, valid_a, raw_a = self.classify_with_prompt(CLASSIFICATION_PROMPT_A,email_text)

        print("\n Running classification prompt B")
        output_b, valid_b, raw_b = self.classify_with_prompt(CLASSIFICATION_PROMPT_B,email_text)

        print("\n Evaluating A vs B ---")
        evaluation = self.evaluate_versions(email_text, output_a, output_b)


        winner = evaluation.get("winner", "A").upper()
        reasoning = evaluation.get("reasoning" , "No reasoning provided.")
        #print result for viewability in console
        print(f"winner: Prompt {winner}")
        print(f"Reasoning: {reasoning}")

        winner_output = output_a if winner == "A" else output_b

        winner_output["metadata"] = winner_output.get("metadata", {})
        winner_output["metadata"].update({
            "evaluation_reasoning": reasoning,
            "winning_prompt": winner
        })


        return winner_output

    # def classify(self, email_text: str) -> dict:
    #     prompt = CLASSIFICATION_PROMPT.format(email_text=email_text)
    #     result = self.llm.chat(SYSTEM_PROMPT, prompt)
    #     try:
    #         return json.loads(result)
    #     except Exception:
    #         return {"error": "Failed to parse LLM response", "raw_output": result}

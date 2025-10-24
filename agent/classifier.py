import json
from .prompt_manager import (
    SYSTEM_PROMPT,
    CLASSIFICATION_PROMPT_A,
    CLASSIFICATION_PROMPT_B,
    EVALUATION_PROMPT
)

class EmailClassifier:
    
    #init with AB test option or exlude "self reflection" and go with one prompt (less expensive usage)
    def __init__(self, llm_client, mode="AB"):
        """
        mode can be:
        - "A"  -> only run prompt A
        - "B"  -> only run prompt B
        - "AB" -> run both and evaluate
        """
        self.llm = llm_client
        self.mode = mode.upper()


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
            output_b = json.dumps(output_b,indent=2),
        )
        eval_result = self.llm.chat("You are a fair and strict Evaluator", eval_prompt)
        try:
            return json.loads(eval_result)
        except Exception:
            return {"winner": "A", "reasoning": "Evaluation failed, defaulted to A."}
    
    #A/B test OR single prompt mode
    def classify(self,email_text: str):
        #A/B Test
        if self.mode == "AB":
            #print process steps
            print("\n Running classification prompt A")
            output_a, valid_a, raw_a = self.classify_with_prompt(CLASSIFICATION_PROMPT_A,email_text)

            print("\n Running classification prompt B")
            output_b, valid_b, raw_b = self.classify_with_prompt(CLASSIFICATION_PROMPT_B,email_text)

            print("\n Evaluating A vs B.")
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
        

        elif self.mode in ["A","B"]:
            
            prompt_to_use = CLASSIFICATION_PROMPT_A if self.mode == "A" else CLASSIFICATION_PROMPT_B
            print(f" Running Classification Prompt {self.mode} Only ")
            output, valid, raw = self.classify_with_prompt(prompt_to_use, email_text)
            output["metadata"] = output.get("metadata", {})
            output["metadata"].update({
                "winning_prompt": self.mode,
                "evaluation_reasoning": "Single prompt mode with A/B test."
            })
            return output
        

        else:
            raise ValueError("Invalid classifier mode. Choose 'A', 'B', or 'AB'.")



# AI Customer Support Email Classifier Agent

## Overview
The AI Customer Support Email Classifier Agent uses OpenAI GPT-3.5-turbo to automatically analyze customer support emails. It classifies the type of inquiry, detects sentiment and urgency, extracts the main issue, and generates a professional response template. The project also includes A/B prompt testing and self-evaluation capabilities to refine accuracy over time.

## Features
- Classifies customer emails into one of the following categories:
  - Technical Issue
  - Billing/Payment
  - Feature Request
  - General Inquiry
  - Complaint
- Extracts additional details such as:
  - Sentiment (positive, neutral, or negative)
  - Urgency (low, medium, or high)
  - Main issue summary
  - Customer or account ID when mentioned
- Generates a professional response template based on classification
- Outputs structured JSON directly to the console
- Supports three classification modes:
  - **A:** Uses Prompt A only
  - **B:** Uses Prompt B only
  - **AB:** Runs both prompts, compares their outputs using a self-reflection step, and selects the most accurate result

## Setup
1. Clone or unzip the project directory.
2. Open a terminal and navigate into the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create and configure your environment file:
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-3.5-turbo
   ```
5. Run the agent:
   ```bash
   python main.py
   ```

## Usage
When you run the program, you will be prompted to select a classification mode:

```
Select classification mode:
A  - Use Prompt A only
B  - Use Prompt B only
AB - Run full A/B evaluation (self-reflect)
Enter mode (A/B/AB):
```

After selecting a mode, paste or type your email into the console and press Enter twice to process.

### Mode Behavior
| Mode | Description | LLM Calls | Evaluation Step |
|------|--------------|-----------|----------------|
| A | Uses Prompt A only | 1 | Skipped |
| B | Uses Prompt B only | 1 | Skipped |
| AB | Runs both A and B, then evaluates which is most accurate | 3 | Performed |

## Example
Input:
```
Hi Support, I can't log into my account. It keeps saying invalid password. Please help ASAP.
```

Output:
```json
{
  "classification": "Technical Issue",
  "sentiment": "negative",
  "urgency": "medium",
  "main_issue": "Files not syncing properly across devices",
  "metadata": {
    "customer_id": "CL-2049",
    "key_points": [
      "Documents not syncing between laptop and phone",
      "Syncing indefinitely after app update"
    ],
    "evaluation_reasoning": "Version B is more accurate and relevant as it provides additional key points that specifically highlight the issues mentioned in the email, such as documents not syncing between laptop and phone and syncing indefinitely after the app update. This extra detail shows a deeper understanding of the customer's problem.",
    "winning_prompt": "B"
  },
  "response_template": "I understand the frustration you must be feeling with the files not syncing properly across your devices. Rest assured, our technical team is actively investigating this issue and working on a solution. Thank you for bringing this to our attention."
}
```

## Architecture
```
ai-support-agent/

-- agent/
   -- classifier.py         # Handles classification, A/B logic, and evaluation
   -- responder.py          # Generates email responses
   -- llm_client.py         # Manages OpenAI API interaction
   -- prompt_manager.py     # Contains prompt templates for A, B, and evaluation
     -- __init__.py

-- examples/                 # Sample customer emails
-- output/                   # Generated example output from testing - at runtime logs are placed in the CLI.
-- main.py                   # CLI entry point
-- requirements.txt
-- .env.example
-- README.md
```

## A/B Testing Logic
When in **AB mode**, the system:
1. Runs both classification prompts independently.
2. Passes both JSON outputs and the original email to a third evaluation prompt.
3. The LLM compares both outputs and selects the version it considers most accurate.
4. The reasoning and chosen version are logged and stored in the final JSON.
5. The selected version’s data is sent to the responder to generate the final message.




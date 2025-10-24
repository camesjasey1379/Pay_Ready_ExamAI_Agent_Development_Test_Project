# AI Customer Support Email Classifier Agent

## Overview
This project uses OpenAI GPT-3.5-turbo to classify customer support emails, detect sentiment and urgency, extract the main issue, and generate a professional response template.

## Features
- Classifies emails into one of the provided categories in the project documentation: Technical Issue, Billing/Payment, Feature Request, General Inquiry, Complaint.
- Extracts sentiment, urgency, and key issue summary.
- Generates a contextual response template.
- Outputs structured JSON to console.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# add your OpenAI key to .env
python main.py
```
Then paste your email text directly and hit Enter twice to process.

## Example
Input:
```
Hi Support, I can't log into my account. Keeps saying invalid password. Please help ASAP.
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

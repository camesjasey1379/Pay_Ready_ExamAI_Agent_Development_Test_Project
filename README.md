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
  "urgency": "high",
  "main_issue": "User unable to log in due to authentication failure",
  "response_template": "Hi there, we're sorry for the login trouble...",
  "metadata": {
    "customer_id": null
  }
}
```

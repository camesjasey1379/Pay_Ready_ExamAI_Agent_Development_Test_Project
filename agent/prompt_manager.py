SYSTEM_PROMPT = """You are an AI support assistant that classifies and analyzes customer support emails.
You must output structured, accurate JSON only.
"""

CLASSIFICATION_PROMPT_A = """
Analyze the following customer email and extract:
classification, sentiment, urgency, main_issue, and metadata.customer_id.
Valid categories: Technical Issue, Billing/Payment, Feature Request, General Inquiry, Complaint.
Output pure JSON only.
Email:
{email_text}
"""



CLASSIFICATION_PROMPT_B = """Analyze the following customer email and extract:
1. Classification: Technical Issue, Billing/Payment, Feature Request, General Inquiry, Complaint
2. Sentiment: positive, neutral, or negative
3. Urgency: low, medium, or high
4. Main issue: concise summary
5. Customer ID if mentioned - AKA 'Account ID'

Return a JSON object with only the following fields:
{{
  "classification": "...",
  "sentiment": "...",
  "urgency": "...",
  "main_issue": "...",
  "metadata": {{
    "customer_id": "...",
    "key_points": ["...","..."]
  }}
}}

Email:
---
{email_text}
---
"""



EVALUATION_PROMPT = """You are a critical evaluator. You will compare two JSON outputs
(A and B) from two classifiers for the same customer email.

Decide which JSON is more accurate and relevant to the email content.
Consider:
1. Is the classification correct and specific?
2. Does the sentiment reflect the customer's tone?
3. Is the urgency realistic based on the text?
4. Is the main_issue concise and true to the email?

Return a JSON with:
{{
  "winner": "A" or "B",
  "reasoning": "short explanation of why that version was better"
}}

Email:
{email_text}

Version A:
{output_a}

Version B:
{output_b}
"""

RESPONSE_PROMPT = """Generate a short professional response template for a {classification} with {sentiment} sentiment and {urgency} urgency.

Main issue:
{main_issue}

Return the response text only.
"""

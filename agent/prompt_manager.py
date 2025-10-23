SYSTEM_PROMPT = """You are an AI support assistant that classifies and analyzes customer support emails.
You must output structured, accurate JSON only.
"""

CLASSIFICATION_PROMPT = """Analyze the following customer email and extract:
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

RESPONSE_PROMPT = """Generate a short professional response template for a {classification} with {sentiment} sentiment and {urgency} urgency.

Main issue:
{main_issue}

Return the response text only.
"""

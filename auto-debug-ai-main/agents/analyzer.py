
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_error(endpoint, method, error_data):
    """
    Uses OpenAI to analyze API error and suggest fix.
    Returns structured JSON.
    """

    prompt = f"""
You are an autonomous API debugging agent.

Analyze this API failure:

API Endpoint: {endpoint}
HTTP Method: {method}
Error Data: {error_data}

Return ONLY valid JSON.
No markdown.
No explanation outside JSON.

Use this structure:

{{
  "reasoning": ["step1", "step2"],
  "issue": "clear issue statement",
  "suggested_fix": "what needs to change",
  "corrected_code": "python code here"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
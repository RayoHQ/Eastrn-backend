from dotenv import load_dotenv
import os
import requests

load_dotenv()

HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
HYPERBOLIC_URL = "https://api.hyperbolic.xyz/v1/completions"

def get_tooltip_from_hyperbolic(term: str, context: str = ""):
    payload = {
        "prompt": f"Provide a concise explanation for the term: '{term}' in the context of: {context}",
        "model": "meta-llama/Meta-Llama-3.1-405B",
        "max_tokens": 64,
        "temperature": 0.7,
        "top_p": 0.9
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HYPERBOLIC_API_KEY}"
    }

    try:
        response = requests.post(HYPERBOLIC_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        explanation = result.get("choices", [{}])[0].get("text", "No explanation available.")
        return explanation.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
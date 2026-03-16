import json
import os


# Load API documentation
def load_api_docs():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up one level
    docs_path = os.path.join(base_dir, "docs", "api.json")

    with open(docs_path, "r") as file:
        return json.load(file)


# Find matching API from stored docs
def find_api_info(endpoint, docs):
    for api_key, api_data in docs.items():
        full_endpoint = api_data["base_url"] + api_data["endpoint"]
        if full_endpoint in endpoint:
            return api_data
    return None


# Main analyzer function
def analyze_error(endpoint, method, error_message, status_code):
    docs = load_api_docs()
    api_info = find_api_info(endpoint, docs)

    # Case 1: API Not Found
    if not api_info:
        return {
            "error_type": "Unknown API",
            "explanation": "The provided endpoint does not match any stored API documentation.",
            "fix": "Verify the endpoint URL or update the API documentation file.",
            "corrected_code": "",
            "reasoning_steps": [
                "Loaded local API documentation",
                "No matching endpoint found",
                "Cannot analyze unknown API"
            ]
        }

    # Case 2: Known Error Code
    error_str = str(status_code)

    if error_str in api_info["common_errors"]:
        explanation = api_info["common_errors"][error_str]

        corrected_code = f"""
import requests

url = "{api_info['base_url']}{api_info['endpoint']}"
headers = {api_info['example_request'].get('headers', {})}

response = requests.{method.lower()}(url, headers=headers)
print(response.json())
"""

        return {
            "error_type": f"HTTP {status_code} Error",
            "explanation": explanation,
            "fix": "Follow the API documentation and correct the request accordingly.",
            "corrected_code": corrected_code.strip(),
            "reasoning_steps": [
                "Loaded API documentation successfully",
                f"Matched endpoint: {api_info['name']}",
                f"Detected status code: {status_code}",
                "Found predefined error explanation in documentation"
            ]
        }

    # Case 3: Unknown Error Code for Known API
    return {
        "error_type": "Unhandled Error",
        "explanation": error_message,
        "fix": "Review API documentation and validate request parameters.",
        "corrected_code": "",
        "reasoning_steps": [
            "API matched from documentation",
            f"Status code {status_code} not predefined",
            "Manual inspection required"
        ]
    }
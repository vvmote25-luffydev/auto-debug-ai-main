import requests
from agents.analyzer import analyze_error


def call_api(endpoint, method="GET", headers=None, body=None):
    try:
        if method.upper() == "GET":
            response = requests.get(endpoint, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(endpoint, json=body, headers=headers)
        else:
            return {"success": False, "error": "Unsupported method"}

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            }

    except Exception as e:
        return {"success": False, "error": str(e)}


def autonomous_debug(endpoint, method="GET"):
    """
    Full autonomous debugging loop
    """

    logs = []

    logs.append("🔎 Attempting initial API call...")
    result = call_api(endpoint, method)

    if result["success"]:
        logs.append("✅ API call successful on first attempt.")
        return {
            "final_status": "success",
            "response": result,
            "logs": logs,
            "ai_analysis": None
        }

    logs.append("⚠ API failed. Sending error to AI analyzer...")

    ai_result = analyze_error(endpoint, method, result)

    logs.append("🤖 AI analysis complete.")
    logs.append("🔁 Retrying API call (demo retry)...")

    retry_result = call_api(endpoint, method)

    if retry_result["success"]:
        logs.append("✅ API call successful after retry.")
        final_status = "success"
    else:
        logs.append("❌ API still failing after retry.")
        final_status = "failed"

    return {
        "final_status": final_status,
        "initial_error": result,
        "retry_result": retry_result,
        "ai_analysis": ai_result,
        "logs": logs
    }
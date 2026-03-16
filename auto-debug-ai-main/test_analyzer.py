from agents.analyzer import analyze_error

error_data = {
    "status_code": 401,
    "error": "Unauthorized"
}

result = analyze_error(
    "https://api.example.com/users",
    "GET",
    error_data
)

print(result)
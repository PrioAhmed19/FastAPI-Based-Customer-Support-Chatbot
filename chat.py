import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What's the price of iPhone?"}
)
print(response.json())
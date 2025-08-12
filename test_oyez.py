import requests


url = "http://localhost:8080/v1/completions"


headers = {"Content-Type": "application/json"}


data = {
    "model": "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
    "prompt": "Explain the concept of gravity in simple terms.",
    "temperature": 0.7,
    "max_tokens": 300,
}


response = requests.post(url, headers=headers, json=data)


print(response.json())
import requests
import json

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
data = {
    "model": "gemma:2b",
    "prompt": "Give me a funny Instagram caption about coffee.",
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)

print("\n--- Ollama Response ---\n")
for line in response.iter_lines():
    if line:
        try:
            parsed = json.loads(line)
            print(parsed.get("response", ""), end="", flush=True)
        except json.JSONDecodeError:
            print("\n[!] JSON parsing error.")
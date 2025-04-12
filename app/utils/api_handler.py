import requests
import os

def get_chatgpt_response(prompt):
    api_key = os.getenv("CHATGPT_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    response = requests.post(url, headers=headers, json=payload, stream=True)
    return response

def get_ollama_response(prompt):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.2",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    response = requests.post(url, headers=headers, json=payload, stream=True)
    return response
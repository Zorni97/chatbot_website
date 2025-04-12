from flask import Flask, render_template, request, Response
import requests
import json
import os

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL_OPTIONS = {
    "ChatGPT": "gpt-4o-mini",
    "Ollama": "llama3.2"
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Load API key from .env

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    model = request.form['model']
    model_name = MODEL_OPTIONS.get(model)

    if model_name == "Ollama":
        return Response(stream_ollama_response(question), mimetype='text/event-stream')
    else:
        return Response(stream_chatgpt_response(question), mimetype='text/event-stream')

def stream_ollama_response(question):
    messages = [{"role": "user", "content": question}]
    payload = {
        "model": "llama3.2",
        "messages": messages,
        "stream": True
    }
    
    with requests.post(OLLAMA_API, json=payload, headers=HEADERS, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield f"data: {data['message']['content']}\n\n"

def stream_chatgpt_response(question):
    messages = [{"role": "user", "content": question}]
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "stream": True
    }
    openai_api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    with requests.post(openai_api_url, json=payload, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    if 'content' in delta:
                        yield f"data: {delta['content']}\n\n"

if __name__ == '__main__':
    app.run(debug=True)
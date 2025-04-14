from flask import Flask, render_template, request, Response, session, jsonify
import requests, json, os, markdown
from dotenv import load_dotenv
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app)

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL_OPTIONS = {
    "ChatGPT": "gpt-4o-mini",
    "Ollama": "llama3.2"
}

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    model = data.get('model')

    session.setdefault('history', [])
    session['history'].append({"role": "user", "content": question})
    model_name = MODEL_OPTIONS.get(model)

    if not model_name:
        return {"error": f"Invalid model: {model}"}, 400

    if model == "Ollama":
        return Response(stream_ollama_response(session['history']), mimetype='text/event-stream')
    else:
        return Response(stream_chatgpt_response(session['history']), mimetype='text/event-stream')

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify({"status": "reset successful"})

def stream_ollama_response(history):
    payload = {
        "model": "llama3.2",
        "messages": history,
        "stream": True
    }
    accumulated = ""

    with requests.post(OLLAMA_API, json=payload, headers=HEADERS, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                content = data.get("message", {}).get("content", "")
                accumulated += content
                yield f"data: {format_response(accumulated)}\n\n"

    session['history'].append({"role": "assistant", "content": accumulated})

def stream_chatgpt_response(history):
    payload = {
        "model": "gpt-4o-mini",
        "messages": history,
        "stream": True
    }
    openai_api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    accumulated = ""

    with requests.post(openai_api_url, json=payload, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                line_content = line.decode('utf-8').strip()
                if line_content == "data: [DONE]":
                    break
                if line_content.startswith("data: "):
                    line_content = line_content[len("data: "):]
                try:
                    data = json.loads(line_content)
                    delta = data['choices'][0].get('delta', {})
                    if 'content' in delta:
                        accumulated += delta['content']
                        yield f"data: {format_response(accumulated)}\n\n"
                except Exception:
                    continue

    session['history'].append({"role": "assistant", "content": accumulated})

def format_response(text):
    html = markdown.markdown(text)
    html = html.replace('$$', '<span class="mathjax">$$').replace('$$', '$$</span>')
    html = html.replace('$', '<span class="mathjax">$').replace('$', '$</span>')
    return html

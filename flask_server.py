import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai import AzureOpenAI

load_dotenv()
app = Flask(__name__)

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

if not OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
    raise ValueError("Missing environment variables. See .env.example")

client = AzureOpenAI(
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

@app.route("/api/secureapi", methods=["POST"])
def secureapi_proxy():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a secure API gateway."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=0.95,
            frequency_penalty=0.7,
        )
        output = response.choices[0].message.content
        # Do not log prompt or full response to disk to preserve privacy
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use a production WSGI server (gunicorn/uvicorn) in real deployments
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

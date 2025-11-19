# SecureAPI Python Project (SOP-compliant)

This project provides:
- A **CLI client** (`sop_client.py`) that calls the SecureAPI via the AzureOpenAI client.
- A **Flask server** (`flask_server.py`) exposing `/api/secureapi` as a proxy to the SecureAPI (SOP).
- A **Streamlit UI** (`streamlit_app.py`) for a quick visual prototype.
- Example environment variables in `.env.example`.

## How this follows the SOP
- Uses environment variables: `OPENAI_API_VERSION`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`.
- Uses `gpt-4o-mini` model (listed in SOP).
- Does not store prompts or responses to disk (no logging to files).
- All keys are read from environment variables and never hard-coded.
- Example client parameters (temperature, top_p, frequency_penalty) match SOP recommendations.

## Quickstart (local)

1. Copy `.env.example` to `.env` and fill the `AZURE_OPENAI_API_KEY`.
2. Create a virtual environment and install deps:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python flask_server.py
   ```
4. In another terminal, run Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```
5. Or run CLI client:
   ```bash
   python sop_client.py
   ```

## Security & Privacy Notes
- Enforce HTTPS when deploying (use a proper hosting / reverse proxy).
- Do not commit `.env` or `AZURE_OPENAI_API_KEY` to source control.
- Use production WAF, rate-limiting, and API key rotation as described in the SOP.
- Consider token limits and usage monitoring per SOP (max tokens per user, key limits).

## Deployment
- For production, use a WSGI server (gunicorn) and an HTTPS-enabled host (Azure App Service, AWS, etc.).
- Use Azure Key Vault or similar to store secrets in production.

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

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

def call_secureapi(prompt: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=0.95,
            frequency_penalty=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling SecureAPI: {e}"

def main():
    print("\n=== SecureAPI Python CLI (SOP Compliant) ===")
    while True:
        prompt = input("\nEnter prompt (or 'exit'): ")
        if prompt.lower() == "exit":
            break
        out = call_secureapi(prompt)
        print("\n--- Response ---")
        print(out)
        print("----------------\n")

if __name__ == "__main__":
    main()

# python
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found in environment (.env).")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) <= 1:
        print("Error: no prompt provided.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])  # <-- define it

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(response.text)
    if len(sys.argv) == 3:
        print(f"User prompt: {sys.argv[2]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
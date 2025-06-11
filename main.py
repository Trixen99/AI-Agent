import os
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types

user_prompt = argv[1]


if len(argv) < 2:
    print("no prompt provided")
    exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
 
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if len(argv) > 2:
    if argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

print(response.text)

    
from google.genai import types
from dotenv import load_dotenv
from prompt import system_prompt
from functions.available_functions import available_functions

def generate_response(client, messages):
    return client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
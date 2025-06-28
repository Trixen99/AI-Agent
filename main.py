import os
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types
#from prompt import system_prompt
#from functions.available_functions import available_functions
from functions.call_function import call_function
from response import generate_response

user_prompt = argv[1]

if len(argv) < 2:
    print("no prompt provided")
    exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
 
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

for loop_count in range(20):
    response = generate_response(client, messages)
    for candidate in response.candidates:
        messages.extend([candidate.content])

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    verbose = False
    if len(argv) > 2:
        if argv[2] == "--verbose":
            verbose = True
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")


    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            called_function = call_function(function_call)
            messages.extend([called_function])
        
            if not called_function.parts[0].function_response.response:
                raise Exception("no response was provided by function")
            elif called_function.parts[0].function_response.response and verbose == True:
                print(f"-> {called_function.parts[0].function_response.response}")
        continue
    else:
        print(response.text)
        break

    
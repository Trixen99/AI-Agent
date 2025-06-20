import os
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types

user_prompt = argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


if len(argv) < 2:
    print("no prompt provided")
    exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and directories in the specified directory along with their sizes and directory status, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory, If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="returns a string which contains the content of a file up to a max of 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file you to return the content from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the selected python file, file selected must be a '.py' file, this function is constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run in python, relative to the working directory. File must end with .py",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Can amend an existing file or create a new one inputting the provided text into the file. if used on an existing file the function will remove any existing content in the file. This function is constrained to the working directory. This function will also create any required parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file you to write to, if the file does not exist a new file will be created relative to the working directory. final file path must be within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text you would like to input into the existing or new file"
            )
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
 
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if len(argv) > 2:
    if argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)

    
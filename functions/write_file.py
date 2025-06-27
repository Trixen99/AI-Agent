import os
from google.genai import types

def write_file(working_directory, file_path, content):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, file_path or ""))]) != os.path.abspath(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    

    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        with open(path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except OSError as error:
        return f"Error: {error}"
    

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


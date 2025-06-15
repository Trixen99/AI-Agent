import os

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


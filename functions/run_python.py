import os
import subprocess


def run_python_file(working_directory, file_path):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, file_path or ""))]) != os.path.abspath(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.exists(path) == False:
            return f'Error: File "{file_path}" not found.'

        if not path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
    
        output = subprocess.run(["python3", path], timeout=30, capture_output=True)
        final = []
        if output.stdout:
            final.append(f"STDOUT:{output.stdout}")
        if output.stderr:
            final.append(f"STDERR:{output.stderr}")
        if output.returncode != 0:
            final.append(f"Process exited with code {final.returncode}")

        if final:
            return "".join(final)
        else:
            return "No output produced"

    except Exception as error:
        return f"Error: executing Python file: {error}"
    
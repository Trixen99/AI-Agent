import os
def get_file_content(working_directory, file_path):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, file_path or ""))]) != os.path.abspath(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(os.path.abspath(os.path.join(working_directory, file_path))):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:
        path = os.path.abspath(os.path.join(working_directory, file_path))
        returnValue = []
        with open(path) as content:
            text = content.read()
            if len(text) > 10000:
                returnValue.append(text[0:10000])
                returnValue.append(f"...File {path} truncated at 10000 characters")
            else:
                returnValue.append(text)
    
        return "".join(returnValue)
    except OSError as error:
        return f"Error: {error}"






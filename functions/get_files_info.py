import os


def get_files_info(working_directory, directory=None):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, directory or ""))]) != os.path.abspath(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(os.path.abspath(os.path.join(working_directory,directory))):
        return ""
    
    
    try:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))
        return_string = []
        directory_list = os.listdir(directory_path)
        if len(directory_list) == 0:
            return f"No files in directory: {directory_path}"
        for item in directory_list:
            item_path = os.path.join(directory_path, item)
            return_string.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

        return "\n".join(return_string)
    except OSError as error:
        return f"Error: {error}"






    
     


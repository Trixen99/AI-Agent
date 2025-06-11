import os


def get_files_info(working_directory, directory=None):
    if os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, directory or ""))]) != os.path.abspath(working_directory):
        print(os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, directory or ""))]))
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    #working_path = os.path.abspath(working_directory)
    #directory_path = os.path.abspath(os.path.join(working_directory, directory or ""))
    #if not directory_path.startswith(working_path):
    #    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    #if not working_path.split("/")[-1] == directory_path.split("/")[-2]:
    #    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


    




    
     




print(get_files_info("/tmp/abc", "/tmp/abc2"))
print("\n")
#print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "pkg"))
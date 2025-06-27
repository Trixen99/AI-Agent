from google.genai import types
from functions.available_functions import function_dictionary
import ast

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    working_directory = "./calculator"
    function = function_dictionary[function_call_part.name]
    arguments = function_call_part.args
    hello = function(working_directory, **arguments)

    print(hello)

    #test_run = ast.literal_eval(new_string)